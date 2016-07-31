from app import app
from errors import registerAPIErrors

registerAPIErrors(app)

# Register routes
import routes

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
