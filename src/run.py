from app import create_app

try:
    app = create_app()
except Exception as e:
    print(f"An error occurred while creating the app: {str(e)}")
    exit(1)

if __name__ == '__main__':
    app.run()