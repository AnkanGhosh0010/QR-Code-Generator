import qrcode
from flask import Flask, request, render_template, send_file
import io
import base64

#flask app
app = Flask(__name__)

# Route for home page
@app.route("/", methods=["GET", "POST"])
def generate_qr():
    qr_image = None
    
    if request.method == "POST":
        data = request.form.get("data")
        
        if data:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=20,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Generate image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 for display
            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            
            # Encode to base64 for HTML display
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            qr_image = f"data:image/png;base64,{img_base64}"
    
    return render_template("index.html", qr_image=qr_image)

# Route for downloading QR code
@app.route("/download", methods=["POST"])
def download_qr():
    data = request.form.get("data")
    
    if data:
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=20,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO for download
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name='qrcode.png'
        )
    
    return "No data provided", 400

if __name__ == "__main__":
    app.run(debug=True)
