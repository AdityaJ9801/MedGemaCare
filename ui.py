"""
Gradio Interactive UI — MedGemma 1.5 4B Medical AI
Covers all endpoints including new multimodal capabilities:
- Text summarization & Q&A
- Medical image analysis (X-ray, CT, MRI, histopathology)
- Longitudinal image comparison
- Anatomical localization
- Lab report extraction
- EHR analysis
- RAG pipeline

Start the FastAPI backend first:  python run.py
Then launch this UI:              python ui.py
"""

import requests
import gradio as gr

API = "http://localhost:8000/api/v1"
TIMEOUT = 180  # seconds per request (increased for image processing)


# ── helpers ────────────────────────────────────────────────────────────────────

def _err(r: requests.Response) -> str:
    try:
        return r.json().get("detail", r.text)
    except Exception:
        return r.text


# ── API wrappers ───────────────────────────────────────────────────────────────

def check_health() -> str:
    try:
        r = requests.get(f"{API}/health", timeout=10)
        d = r.json()
        status  = "🟢 Healthy"    if d.get("status") == "healthy" else "🔴 Unhealthy"
        ml      = "✅ Available"  if d.get("ml_available")        else "❌ Not available"
        model   = "✅ Loaded"     if d.get("model_loaded")        else "⏳ Not loaded"
        return (
            f"**Status:** {status}\n\n"
            f"**ML Dependencies:** {ml}\n\n"
            f"**Model:** {model}\n\n"
            f"**Version:** {d.get('version', 'N/A')}"
        )
    except Exception as e:
        return f"❌ Cannot reach API — is `python run.py` running?\n\n`{e}`"


def summarize(text: str, max_length: int, temperature: float) -> str:
    if not text.strip():
        return "⚠️ Please paste medical report text."
    try:
        r = requests.post(
            f"{API}/summarize",
            json={"text": text, "max_length": max_length, "temperature": temperature},
            timeout=TIMEOUT,
        )
        if r.ok:
            d = r.json()
            return (
                f"**Summary** *(condensed {d['input_length']} → {d['summary_length']} chars)*\n\n"
                f"{d['summary']}"
            )
        return f"❌ {r.status_code}: {_err(r)}"
    except Exception as e:
        return f"❌ {e}"


def analyze(text: str, question: str) -> str:
    if not text.strip() or not question.strip():
        return "⚠️ Provide both the report text and a question."
    try:
        r = requests.post(
            f"{API}/analyze",
            json={"text": text, "question": question},
            timeout=TIMEOUT,
        )
        if r.ok:
            d = r.json()
            return f"**Q:** {d['question']}\n\n**A:** {d['answer']}"
        return f"❌ {r.status_code}: {_err(r)}"
    except Exception as e:
        return f"❌ {e}"


def upload_document(file) -> str:
    if file is None:
        return "⚠️ Please select a PDF or TXT file."
    try:
        with open(file.name, "rb") as fh:
            r = requests.post(
                f"{API}/upload/document",
                files={"file": (file.name, fh)},
                timeout=TIMEOUT,
            )
        if r.ok:
            d = r.json()
            return (
                f"✅ **{d['filename']}** indexed!\n\n"
                f"- Format: `{d['format']}`  |  Size: {d['file_size']:,} bytes\n\n"
                f"- {d['message']}"
            )
        return f"❌ {r.status_code}: {_err(r)}"
    except Exception as e:
        return f"❌ {e}"


def upload_image(file) -> str:
    if file is None:
        return "⚠️ Please select a JPG, PNG, or TIFF image."
    try:
        with open(file.name, "rb") as fh:
            r = requests.post(
                f"{API}/upload/image",
                files={"file": (file.name, fh)},
                timeout=TIMEOUT,
            )
        if r.ok:
            d = r.json()
            return (
                f"✅ **{d['filename']}** processed!\n\n"
                f"- Format: `{d['format']}`  |  Size: {d['file_size']:,} bytes\n\n"
                f"- {d['message']}"
            )
        return f"❌ {r.status_code}: {_err(r)}"
    except Exception as e:
        return f"❌ {e}"


def rag_summarize(query: str, top_k: int) -> str:
    try:
        r = requests.post(
            f"{API}/rag/summarize",
            json={
                "query": query or "Provide a comprehensive summary of the medical report",
                "top_k": top_k,
            },
            timeout=TIMEOUT,
        )
        if r.ok:
            d = r.json()
            return f"**RAG Summary** *({d['summary_length']} chars)*\n\n{d['summary']}"
        return f"❌ {r.status_code}: {_err(r)}"
    except Exception as e:
        return f"❌ {e}"


def rag_question(question: str, top_k: int):
    if not question.strip():
        return "⚠️ Please enter a question.", ""
    try:
        r = requests.post(
            f"{API}/rag/question",
            json={"question": question, "top_k": top_k},
            timeout=TIMEOUT,
        )
        if r.ok:
            d = r.json()
            answer = (
                f"**Q:** {d['question']}\n\n"
                f"**A:** {d['answer']}\n\n"
                f"*Chunks used: {d['num_chunks_used']}*"
            )
            chunks = "\n\n---\n\n".join(d.get("relevant_chunks") or []) or "No chunks returned."
            return answer, chunks
        return f"❌ {r.status_code}: {_err(r)}", ""
    except Exception as e:
        return f"❌ {e}", ""


# ── MedGemma 1.5 4B New Features ──────────────────────────────────────────────

def analyze_image(file, query: str) -> str:
    if file is None:
        return "⚠️ Please select a medical image."
    try:
        with open(file.name, "rb") as fh:
            r = requests.post(
                f"{API}/analyze/image",
                files={"file": (file.name, fh)},
                params={"query": query},
                timeout=TIMEOUT,
            )
        if r.ok:
            d = r.json()
            return (
                f"**Image:** {d['filename']} ({d['image_type']})\n\n"
                f"**Analysis:**\n\n{d['analysis']}"
            )
        return f"❌ {r.status_code}: {_err(r)}"
    except Exception as e:
        return f"❌ {e}"


def analyze_longitudinal(files, query: str) -> str:
    if not files or len(files) < 2:
        return "⚠️ Please select at least 2 images for comparison."
    try:
        file_tuples = []
        for f in files:
            file_tuples.append(("files", (f.name, open(f.name, "rb"))))
        r = requests.post(
            f"{API}/analyze/longitudinal",
            files=file_tuples,
            params={"query": query},
            timeout=TIMEOUT,
        )
        for _, (_, fh) in file_tuples:
            fh.close()
        if r.ok:
            d = r.json()
            return (
                f"**Compared {d['num_images']} images:** {', '.join(d['filenames'])}\n\n"
                f"**Analysis:**\n\n{d['analysis']}"
            )
        return f"❌ {r.status_code}: {_err(r)}"
    except Exception as e:
        return f"❌ {e}"


def localize_anatomy(file, query: str) -> str:
    if file is None:
        return "⚠️ Please select a chest X-ray image."
    try:
        with open(file.name, "rb") as fh:
            r = requests.post(
                f"{API}/localize/anatomy",
                files={"file": (file.name, fh)},
                params={"query": query},
                timeout=TIMEOUT,
            )
        if r.ok:
            d = r.json()
            return (
                f"**Image:** {d['filename']} (Size: {d['image_size']})\n\n"
                f"**Localization Results:**\n\n{d['raw_response']}"
            )
        return f"❌ {r.status_code}: {_err(r)}"
    except Exception as e:
        return f"❌ {e}"


def extract_lab_data(text: str) -> str:
    if not text.strip():
        return "⚠️ Please paste lab report text."
    try:
        r = requests.post(
            f"{API}/extract/lab",
            json={"text": text},
            timeout=TIMEOUT,
        )
        if r.ok:
            d = r.json()
            return (
                f"**Extracted from {d['input_length']} chars:**\n\n"
                f"```json\n{d['raw_response']}\n```"
            )
        return f"❌ {r.status_code}: {_err(r)}"
    except Exception as e:
        return f"❌ {e}"


def analyze_ehr(ehr_text: str, query: str) -> str:
    if not ehr_text.strip():
        return "⚠️ Please paste EHR data."
    try:
        r = requests.post(
            f"{API}/analyze/ehr",
            json={"ehr_text": ehr_text, "query": query},
            timeout=TIMEOUT,
        )
        if r.ok:
            d = r.json()
            return (
                f"**Analyzed {d['input_length']} chars of EHR data:**\n\n"
                f"{d['analysis']}"
            )
        return f"❌ {r.status_code}: {_err(r)}"
    except Exception as e:
        return f"❌ {e}"


# ── Gradio UI ──────────────────────────────────────────────────────────────────

THEME = gr.themes.Soft(primary_hue="blue", neutral_hue="slate")

with gr.Blocks(theme=THEME, title="🏥 MedGemma 1.5 4B Medical AI") as demo:

    gr.Markdown(
        "# 🏥 MedGemma 1.5 4B Medical AI\n"
        "> **New Features:** Medical imaging (CT/MRI/X-ray) · Longitudinal comparison · "
        "Anatomical localization · Lab data extraction · EHR analysis · RAG Pipeline\n\n"
        "Make sure `python run.py` is running before using any feature below."
    )

    with gr.Tabs():

        # ── Tab 1 · Health Check ───────────────────────────────────────────────
        with gr.Tab("🔍 Health Check"):
            gr.Markdown("Verify that the API server and ML model are operational.")
            health_out = gr.Markdown(value="*Click the button to check.*")
            gr.Button("Check API Health", variant="primary").click(
                check_health, outputs=health_out
            )

        # ── Tab 2 · Summarize ──────────────────────────────────────────────────
        with gr.Tab("📝 Summarize Report"):
            gr.Markdown("Paste a medical report to generate a concise AI summary.")
            with gr.Row():
                with gr.Column(scale=1):
                    sum_text = gr.Textbox(label="Medical Report Text", lines=10,
                                          placeholder="Paste the full report here…")
                    sum_len  = gr.Slider(50, 2048, value=512, step=50,
                                         label="Max Summary Length (chars)")
                    sum_temp = gr.Slider(0.1, 1.0, value=0.7, step=0.05,
                                         label="Temperature")
                    sum_btn  = gr.Button("Generate Summary", variant="primary")
                with gr.Column(scale=1):
                    sum_out = gr.Markdown(label="Summary Output")
            sum_btn.click(summarize, inputs=[sum_text, sum_len, sum_temp], outputs=sum_out)

        # ── Tab 3 · Question & Answer ──────────────────────────────────────────
        with gr.Tab("❓ Question & Answer"):
            gr.Markdown("Ask specific questions about a medical report passage.")
            with gr.Row():
                with gr.Column(scale=1):
                    qa_text = gr.Textbox(label="Medical Report Text", lines=8,
                                         placeholder="Paste report here…")
                    qa_q    = gr.Textbox(label="Your Question",
                                         placeholder="What is the patient's diagnosis?")
                    qa_btn  = gr.Button("Get Answer", variant="primary")
                with gr.Column(scale=1):
                    qa_out  = gr.Markdown(label="Answer")
            qa_btn.click(analyze, inputs=[qa_text, qa_q], outputs=qa_out)

        # ── Tab 4 · Upload Document ────────────────────────────────────────────
        with gr.Tab("📂 Upload Document"):
            gr.Markdown(
                "Upload a **PDF** or **TXT** medical document.\n"
                "It will be extracted and indexed into the RAG vector store."
            )
            doc_file = gr.File(label="Select Document", file_types=[".pdf", ".txt"])
            doc_out  = gr.Markdown()
            gr.Button("Upload & Index", variant="primary").click(
                upload_document, inputs=doc_file, outputs=doc_out
            )

        # ── Tab 5 · Upload Image ───────────────────────────────────────────────
        with gr.Tab("🖼️ Upload Image"):
            gr.Markdown(
                "Upload a medical image (**JPG, PNG, TIFF**).\n"
                "OCR will extract text, which is then indexed for RAG."
            )
            img_file = gr.File(label="Select Image",
                               file_types=[".jpg", ".jpeg", ".png", ".tiff"])
            img_out  = gr.Markdown()
            gr.Button("Upload & Extract Text", variant="primary").click(
                upload_image, inputs=img_file, outputs=img_out
            )

        # ── Tab 6 · RAG Summarize ──────────────────────────────────────────────
        with gr.Tab("🔗 RAG Summarize"):
            gr.Markdown(
                "Generate a summary using **Retrieval-Augmented Generation** over all "
                "previously indexed documents."
            )
            with gr.Row():
                with gr.Column(scale=1):
                    rs_query = gr.Textbox(
                        label="Retrieval Query",
                        value="Provide a comprehensive summary of the medical report",
                        lines=2,
                    )
                    rs_topk = gr.Slider(1, 20, value=5, step=1, label="Top-K Chunks")
                    rs_btn  = gr.Button("Generate RAG Summary", variant="primary")
                with gr.Column(scale=1):
                    rs_out = gr.Markdown(label="RAG Summary Output")
            rs_btn.click(rag_summarize, inputs=[rs_query, rs_topk], outputs=rs_out)

        # ── Tab 7 · RAG Question & Answer ─────────────────────────────────────
        with gr.Tab("🧠 RAG Q&A"):
            gr.Markdown(
                "Ask questions answered by retrieving relevant passages from **indexed documents**."
            )
            with gr.Row():
                with gr.Column(scale=1):
                    rq_q    = gr.Textbox(label="Question",
                                          placeholder="What are the main findings?")
                    rq_topk = gr.Slider(1, 20, value=5, step=1, label="Top-K Chunks")
                    rq_btn  = gr.Button("Ask with RAG", variant="primary")
                with gr.Column(scale=1):
                    rq_ans    = gr.Markdown(label="Answer")
                    rq_chunks = gr.Textbox(label="Retrieved Chunks (context)",
                                           lines=8, interactive=False)
            rq_btn.click(rag_question, inputs=[rq_q, rq_topk],
                         outputs=[rq_ans, rq_chunks])

        # ══════════════════════════════════════════════════════════════════════
        # MedGemma 1.5 4B NEW CAPABILITIES
        # ══════════════════════════════════════════════════════════════════════

        # ── Tab 8 · Medical Image Analysis ─────────────────────────────────────
        with gr.Tab("🩻 Image Analysis"):
            gr.Markdown(
                "**MedGemma 1.5 4B** native medical image analysis.\n"
                "Supports: X-ray, CT slices, MRI slices, histopathology, DICOM, NIfTI."
            )
            with gr.Row():
                with gr.Column(scale=1):
                    ia_file = gr.File(label="Select Medical Image",
                                      file_types=[".jpg", ".jpeg", ".png", ".tiff", ".dcm"])
                    ia_query = gr.Textbox(
                        label="Analysis Query",
                        value="Describe this medical image in detail, including any abnormalities.",
                        lines=2,
                    )
                    ia_btn = gr.Button("Analyze Image", variant="primary")
                with gr.Column(scale=1):
                    ia_out = gr.Markdown(label="Analysis Result")
            ia_btn.click(analyze_image, inputs=[ia_file, ia_query], outputs=ia_out)

        # ── Tab 9 · Longitudinal Comparison ────────────────────────────────────
        with gr.Tab("📊 Longitudinal"):
            gr.Markdown(
                "Compare **multiple images** over time (e.g., current vs prior X-rays).\n"
                "Upload at least 2 images."
            )
            with gr.Row():
                with gr.Column(scale=1):
                    lo_files = gr.File(label="Select Multiple Images (2+)",
                                       file_count="multiple",
                                       file_types=[".jpg", ".jpeg", ".png", ".tiff", ".dcm"])
                    lo_query = gr.Textbox(
                        label="Comparison Query",
                        value="Compare these images and describe any changes or progression over time.",
                        lines=2,
                    )
                    lo_btn = gr.Button("Compare Images", variant="primary")
                with gr.Column(scale=1):
                    lo_out = gr.Markdown(label="Longitudinal Analysis")
            lo_btn.click(analyze_longitudinal, inputs=[lo_files, lo_query], outputs=lo_out)

        # ── Tab 10 · Anatomical Localization ───────────────────────────────────
        with gr.Tab("📍 Localization"):
            gr.Markdown(
                "**Bounding box localization** of anatomical features and findings in chest X-rays."
            )
            with gr.Row():
                with gr.Column(scale=1):
                    loc_file = gr.File(label="Select Chest X-ray",
                                       file_types=[".jpg", ".jpeg", ".png", ".tiff", ".dcm"])
                    loc_query = gr.Textbox(
                        label="Localization Query",
                        value="Identify and localize anatomical features and any abnormalities with bounding boxes.",
                        lines=2,
                    )
                    loc_btn = gr.Button("Localize Anatomy", variant="primary")
                with gr.Column(scale=1):
                    loc_out = gr.Markdown(label="Localization Results")
            loc_btn.click(localize_anatomy, inputs=[loc_file, loc_query], outputs=loc_out)

        # ── Tab 11 · Lab Data Extraction ───────────────────────────────────────
        with gr.Tab("🧪 Lab Extraction"):
            gr.Markdown(
                "Extract **structured data** (values, units, reference ranges) from unstructured lab reports."
            )
            with gr.Row():
                with gr.Column(scale=1):
                    lab_text = gr.Textbox(
                        label="Lab Report Text",
                        placeholder="Paste lab report text here...\n\nExample:\nHemoglobin: 14.2 g/dL (Normal: 12-16)\nWBC: 8500 /uL (Normal: 4000-11000)",
                        lines=10,
                    )
                    lab_btn = gr.Button("Extract Lab Data", variant="primary")
                with gr.Column(scale=1):
                    lab_out = gr.Markdown(label="Extracted Data")
            lab_btn.click(extract_lab_data, inputs=lab_text, outputs=lab_out)

        # ── Tab 12 · EHR Analysis ──────────────────────────────────────────────
        with gr.Tab("📋 EHR Analysis"):
            gr.Markdown(
                "Analyze **Electronic Health Record** text data for clinical insights."
            )
            with gr.Row():
                with gr.Column(scale=1):
                    ehr_text = gr.Textbox(
                        label="EHR Text Data",
                        placeholder="Paste EHR notes, clinical history, medications, etc.",
                        lines=8,
                    )
                    ehr_query = gr.Textbox(
                        label="Analysis Query",
                        value="Summarize the key clinical findings and provide relevant insights.",
                        lines=2,
                    )
                    ehr_btn = gr.Button("Analyze EHR", variant="primary")
                with gr.Column(scale=1):
                    ehr_out = gr.Markdown(label="EHR Analysis")
            ehr_btn.click(analyze_ehr, inputs=[ehr_text, ehr_query], outputs=ehr_out)

    gr.Markdown(
        "---\n"
        "💡 **MedGemma 1.5 4B Capabilities:**\n"
        "- 🩻 **Image Analysis:** X-ray, CT, MRI, histopathology\n"
        "- 📊 **Longitudinal:** Compare images over time\n"
        "- 📍 **Localization:** Bounding boxes for anatomical features\n"
        "- 🧪 **Lab Extraction:** Structured data from lab reports\n"
        "- 📋 **EHR:** Clinical insights from health records\n"
        "- 📂 **RAG:** Upload & query documents\n\n"
        "📚 Full API docs: [http://localhost:8000/docs](http://localhost:8000/docs)"
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)


