from work_tracker import create_app
app = create_app()
app.run("127.0.0.1", 5000, True)
