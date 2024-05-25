<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tomato Disease Classifier</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>Tomato Disease Classifier</h1>
        </header>
        <section class="form-section">
            <h2>Predict Tomato Disease from Image</h2>
            <form action="/predict" method="post" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="file">Upload an image:</label>
                    <input type="file" id="file" name="file" accept="image/*">
                </div>
                <div class="form-group">
                    <label for="url">Or enter an image URL:</label>
                    <input type="url" id="url" name="url" placeholder="https://example.com/image.jpg">
                </div>
                <button type="submit">Upload or Enter URL and Predict</button>
            </form>
        </section>
        <hr>
        <section class="form-section">
            <h2>Ask a Question</h2>
            <form action="/generate" method="post">
                <div class="form-group">
                    <label for="question">Ask a question about tomato diseases:</label>
                    <input type="text" id="question" name="question" required>
                </div>
                <button type="submit">Generate Response</button>
            </form>
        </section>
        {% if diagnosis %}
        <div class="result">
            <h2>Diagnosis</h2>
            <p>{{ diagnosis }}</p>
        </div>
        {% endif %}
        {% if generated_response %}
        <div class="result">
            <h2>Generated Response</h2>
            <p>Question: {{ question }}</p>
            <div>Response: {{ generated_response | safe }}</div>
        </div>
        {% endif %}
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
            <div class="flash-messages">
                {% for category, message in messages %}
                <div class="flash alert alert-{{ category }}">
                    {{ message }}
                </div>
                {% endfor %}
            </div>
            {% endif %}
        {% endwith %}
    </div>
</body>
</html>
