from typing import Union
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.dynamic import AppenderQuery


def resolve_instrumented_attribute(attribute):
    """
    Resolves an InstrumentedAttribute to its actual value.
    """
    if isinstance(attribute, InstrumentedAttribute):
        return (
            None  # Skip InstrumentedAttributes if they aren't directly needed
        )
    return attribute


def extract_model_data(model):
    """
    Extracts only the meaningful data from a SQLAlchemy model, excluding internal attributes.
    """
    return {
        column.name: getattr(model, column.name)
        for column in model.__table__.columns
    }


def make_serializable(
    data: Union[list, tuple, dict, str, int, float, bool, type(None)],
    visited=None,
) -> Union[dict, str]:
    """
    Recursively converts data into JSON-serializable types.
    Handles SQLAlchemy objects and their relationships, avoiding circular references.

    Args:
        data (Union[list, tuple, dict, str, int, float, bool, type): the original data format
        visited (_type_, optional): checks if the attribute node has been visited before. Defaults to None.

    Returns:
        Union[dict, str]: the serialized version of the object including nodes.
    """
    if visited is None:
        visited = set()

    if isinstance(data, (list, tuple)):
        return [make_serializable(item, visited) for item in data]
    elif isinstance(data, dict):
        return {
            str(key): make_serializable(
                resolve_instrumented_attribute(value), visited
            )
            for key, value in data.items()
        }
    elif isinstance(data, AppenderQuery):  # Handle dynamic relationships
        # Fetch all data from the query
        return [make_serializable(item, visited) for item in data.all()]
    elif hasattr(data, "__tablename__"):  # Check if it's an SQLAlchemy model
        obj_id = id(data)
        if obj_id in visited:  # Avoid re-serializing already visited objects
            return f"<CircularReference {data.__class__.__name__}>"
        visited.add(obj_id)

        # Extract core attributes of the SQLAlchemy model
        result = extract_model_data(data)

        # Add relationships
        for (
            relationship_name,
            relationship_property,
        ) in data.__mapper__.relationships.items():
            related_data = getattr(data, relationship_name, None)

            if isinstance(
                related_data, AppenderQuery
            ):  # Handle dynamic relationships
                result[relationship_name] = [
                    extract_model_data(item) for item in related_data.all()
                ]
            elif isinstance(
                related_data, (list, tuple)
            ):  # Relationship returning multiple objects
                result[relationship_name] = [
                    extract_model_data(item) for item in related_data
                ]
            elif related_data is not None:  # Single related object
                result[relationship_name] = extract_model_data(related_data)
            else:
                result[relationship_name] = None  # Relationship not populated

        return result
    elif hasattr(data, "__dict__"):  # Convert custom objects to a dict
        obj_id = id(data)
        if obj_id in visited:  # Avoid circular references in custom objects
            return f"<CircularReference {data.__class__.__name__}>"
        visited.add(obj_id)
        return make_serializable(data.__dict__, visited)
    elif isinstance(data, (str, int, float, bool, type(None))):  # Basic types
        return data
    else:
        return str(data)  # Fallback: Convert to string
