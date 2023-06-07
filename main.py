from app.core.app_builder import build_app

app = build_app()

app.run(host="0.0.0.0", port=5000, debug=True)
