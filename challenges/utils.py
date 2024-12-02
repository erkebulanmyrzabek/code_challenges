import subprocess


def check_solution(solution_code, test_cases):
    results = []
    for test_case in test_cases:
        input_data = test_case.input_data
        expected_output = test_case.expected_output
        try:
            process = subprocess.Popen(['python3', '-c', solution_code],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(input=input_data.encode())
            output = stdout.decode().strip()

            if output == expected_output:
                results.append(True)
            else:
                results.append(False)
        except Exception as e:
            results.append(False)
            print(e)
    return all(results)



from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os


def generate_certificate(user, challenge):
    certificates_dir = os.path.join('media', 'certificates')

    if not os.path.exists(certificates_dir):
        os.makedirs(certificates_dir)

    filename = os.path.join(certificates_dir, f"{user.username}_{challenge.id}_certificate.pdf")

    c = canvas.Canvas(filename, pagesize=letter)

    c.setStrokeColor(colors.black)
    c.setLineWidth(5)
    c.rect(50, 100, 500, 300)

    logo_path = 'static/logo.png'  # Путь к логотипу
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 60, 380, width=100, height=100)

    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(300, 450, f"СЕРТИФИКАТ")

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(300, 410, f"ПОЗДРАВЛЯЕМ!")

    c.setFont("Helvetica", 14)
    c.drawString(100, 350, f"Этот сертификат подтверждает, что")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 320, f"{user.username}")
    c.setFont("Helvetica", 14)
    c.drawString(100, 300, f"успешно завершил задачу:")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 270, f"{challenge.title}")

    c.setFont("Helvetica", 12)

    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.line(50, 150, 550, 150)

    c.setFont("Helvetica", 12)
    c.drawString(100, 120, "Подпись преподавателя")

    c.save()

    return filename

