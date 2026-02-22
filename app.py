from fastapi import FastAPI, UploadFile, File
import os
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

# ---------- App Config ----------
app = FastAPI(
    title="Welding Defect Generator",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

# ---------- Create folders ----------
os.makedirs("uploads", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ---------- CLEAN Swagger UI ----------
@app.get("/docs", include_in_schema=False)
def custom_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Welding Defect Generator",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "defaultModelExpandDepth": -1,
            "docExpansion": "list",
            "tryItOutEnabled": True
        }
    )

@app.get("/", include_in_schema=False)
def root():
    return upload_page()

# ---------- Minimal OpenAPI ----------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Welding Defect Generator",
        version="1.0.0",
        description="",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ---------- UPLOAD PAGE WITH MODERN UI ----------
@app.get("/upload-page", include_in_schema=False)
def upload_page():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welding Defect Detection Report Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: #ffffff;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center;
                width: 400px;
            }
            h1 {
                color: #333333;
                margin-bottom: 30px;
                font-size: 22px;
            }
            input[type="file"] {
                margin: 20px 0;
                padding: 10px;
                width: 100%;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
            button {
                background-color: #007bff;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                width: 100%;
            }
            button:hover {
                background-color: #0056b3;
            }
            a {
                display: inline-block;
                margin-top: 15px;
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welding Defect Detection Report Generator</h1>
            <form action="/upload/" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/jpeg" required>
                <button type="submit">Upload & Generate Report</button>
            </form>
            <a href="/docs" target="_blank">Swagger Docs</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# ---------- UPLOAD IMAGE ----------
@app.post("/upload/", summary="Upload welding image")
async def upload_image(file: UploadFile = File(..., description="Upload JPG welding image")):
    import shutil
    # ---------- Heavy imports inside endpoint ----------
    from detector import detect_defect
    from explain import classify_weld, generate_explanation
    from report import generate_pdf

    # ---------- Save uploaded file ----------
    image_path = os.path.join("uploads", file.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------- Detect defects ----------
    detections = detect_defect(image_path)
    status = classify_weld(detections)

    if detections:
        defect = detections[0]["defect"]
        confidence = detections[0]["confidence"]
        explanation = generate_explanation(defect, confidence)
    else:
        defect = "None"
        confidence = "N/A"
        explanation = "No defect detected."

    # ---------- Generate PDF ----------
    report_path = f"reports/{file.filename}.pdf"
    generate_pdf(
        {
            "status": status,
            "defect": defect,
            "confidence": confidence,
            "explanation": explanation,
            "image": image_path
        },
        report_path
    )

    # ---------- Return HTML with clickable download link ----------
    download_link = f"/download-report/{file.filename}"
    html_response = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload Complete</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                background-color: #ffffff;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center;
                width: 400px;
            }}
            h2 {{ color: #333; }}
            a {{
                display: inline-block;
                margin-top: 20px;
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 6px;
            }}
            a:hover {{ background-color: #0056b3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Upload Successful!</h2>
            <p>Click below to download your PDF report:</p>
            <a href="{download_link}" target="_blank">Download PDF</a>
            <br><br>
            <a href="/upload-page">Upload Another Image</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_response)

# ---------- DOWNLOAD REPORT ----------
@app.get("/download-report/{filename}", include_in_schema=False)
def download_report(filename: str):
    report_path = f"reports/{filename}.pdf"
    return FileResponse(
        path=report_path,
        media_type="application/pdf",
        filename=f"{filename}.pdf"
    )
