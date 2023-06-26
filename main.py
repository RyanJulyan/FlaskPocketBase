from app.core.app_builder import build_app

app = build_app(health_check_kwargs={"dynamic_health_check_kwargs": "working"})

app.run(host="0.0.0.0", port=5000)
