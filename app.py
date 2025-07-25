
import streamlit as st
from fpdf import FPDF
import datetime
import os

st.set_page_config(page_title="Codificador VIH", page_icon="🧬")

st.title("🧬 Codificador VIH - MINSAL")

# Función para generar el código VIH
def generar_codigo(nombre, rut, fecha_nac):
    nombres = nombre.strip().upper().split()
    iniciales = []

    if len(nombres) == 2:
        iniciales = [nombres[0][0], nombres[1][0], '#']
    elif len(nombres) >= 3:
        apellidos = nombres[1:]
        iniciales = [nombres[0][0], apellidos[0][0], apellidos[1][0] if len(apellidos) > 1 else '#']
    else:
        iniciales = ['X', 'X', 'X']

    try:
        f_nac = datetime.datetime.strptime(fecha_nac, "%d/%m/%Y")
        f_cod = f_nac.strftime("%d%m%y")
    except:
        return None, "Fecha nacimiento inválida"

    rut = rut.replace(".", "").replace("-", "")
    if len(rut) < 2:
        return None, "RUT inválido"
    rut_num = rut[:-1]
    digito = rut[-1].upper()

    if not rut_num.isdigit():
        return None, "RUT inválido"

    ultimos3 = rut_num[-3:]
    codigo = "".join(iniciales) + f_cod + ultimos3 + digito
    return codigo, None

# Función para generar el PDF
def exportar_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_title("Codificación VIH")

    pdf.cell(200, 10, txt="CÓDIGO DE IDENTIFICACIÓN VIH", ln=True, align="C")
    pdf.ln(10)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    nombre_archivo = f"VIH_COD_{data['Código VIH']}.pdf"
    pdf.output(nombre_archivo)
    return nombre_archivo

# Formulario
with st.form("formulario_vih"):
    nombre = st.text_input("Nombre completo (nombre + apellidos)")
    rut = st.text_input("RUT (sin puntos, con guión)")
    fecha_nac = st.text_input("Fecha de nacimiento (dd/mm/aaaa)")
    fecha_atencion = st.text_input("Fecha de atención", value=datetime.datetime.today().strftime("%d/%m/%Y"))
    submitted = st.form_submit_button("Generar Código y PDF")

    if submitted:
        if not all([nombre, rut, fecha_nac]):
            st.error("Todos los campos son obligatorios.")
        else:
            codigo, error = generar_codigo(nombre, rut, fecha_nac)
            if error:
                st.error(error)
            else:
                datos = {
                    "Fecha de atención": fecha_atencion,
                    "Fecha de nacimiento": fecha_nac,
                    "RUT": rut,
                    "Código VIH": codigo
                }
                pdf_path = exportar_pdf(datos)
                with open(pdf_path, "rb") as file:
                    st.success(f"Código VIH generado: **{codigo}**")
                    st.download_button("📄 Descargar PDF", file, file_name=pdf_path, mime="application/pdf")
