from pathlib import Path
import textwrap


APP_DIR = Path(__file__).resolve().parents[1]
OUTPUT = APP_DIR / "static" / "autodeploy_interview_questions_answers.pdf"

TITLE = "AutoDeploy Interview Questions and Answers"
SUBTITLE = "FastAPI, Docker, Kubernetes, CI/CD, Prometheus, and Grafana"

SECTIONS = [
    (
        "Project Overview",
        [
            (
                "What problem does AutoDeploy solve?",
                "AutoDeploy demonstrates a production-style delivery pipeline for a FastAPI service. It shows how code can be tested, containerized, deployed, monitored, and rolled back using common DevOps tools.",
            ),
            (
                "How would you explain the architecture in one minute?",
                "A developer pushes code to GitHub. GitHub Actions runs tests, builds a Docker image, pushes it to a registry, and updates a Kubernetes deployment. Kubernetes runs multiple replicas, while Prometheus and Grafana provide metrics and dashboards.",
            ),
            (
                "Why did you choose FastAPI?",
                "FastAPI is lightweight, fast, easy to document with OpenAPI, and a good fit for API-first services. It also makes validation simple through Pydantic models.",
            ),
        ],
    ),
    (
        "CI/CD",
        [
            (
                "What happens when a pull request or push is made?",
                "The pipeline installs dependencies, runs pytest, builds the Docker image, pushes versioned tags, and deploys the new image when the checks pass.",
            ),
            (
                "Why should tests run before Docker build and deploy?",
                "Tests catch regressions early. If tests fail, the pipeline stops before publishing or deploying a broken image.",
            ),
            (
                "How do you make deployments traceable?",
                "Tag images with both latest and the commit SHA. The SHA tag links a running container back to the exact source version.",
            ),
        ],
    ),
    (
        "Docker",
        [
            (
                "Why use a multi-stage Dockerfile?",
                "It keeps the final image smaller and cleaner by separating dependency installation from the runtime image.",
            ),
            (
                "Why run the container as a non-root user?",
                "It reduces the impact of a container compromise because the process has fewer privileges inside the container.",
            ),
            (
                "Why should cloud platforms use a dynamic port?",
                "Platforms like Render provide the port through an environment variable. Binding only to a hard-coded port can make the service unreachable.",
            ),
        ],
    ),
    (
        "Kubernetes",
        [
            (
                "What is the purpose of a Kubernetes Deployment?",
                "A Deployment manages replicas, rollout strategy, self-healing, and updates for application pods.",
            ),
            (
                "What is the difference between liveness and readiness probes?",
                "Liveness checks whether a container should be restarted. Readiness checks whether a pod should receive traffic.",
            ),
            (
                "How does Kubernetes support zero-downtime deployment?",
                "Rolling updates replace old pods gradually while keeping enough healthy replicas available to serve traffic.",
            ),
        ],
    ),
    (
        "Monitoring",
        [
            (
                "What does Prometheus collect from this app?",
                "It scrapes HTTP metrics such as request count, request duration, status codes, and in-progress requests from the metrics endpoint.",
            ),
            (
                "What would you monitor first in production?",
                "Request rate, error rate, latency percentiles, CPU, memory, pod restarts, and deployment rollout status.",
            ),
            (
                "How would you investigate a sudden spike in errors?",
                "Check recent deployments, inspect logs, compare error rate and latency graphs, and roll back if the new release is the likely cause.",
            ),
        ],
    ),
]


def pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def page_stream(lines):
    y = 760
    commands = ["BT", "/F1 12 Tf", "50 760 Td"]
    first = True
    for text, size, gap in lines:
        if not first:
            y -= gap
            commands.append(f"50 {y} Td")
        commands.append(f"/F1 {size} Tf")
        commands.append(f"({pdf_escape(text)}) Tj")
        first = False
    commands.append("ET")
    return "\n".join(commands).encode("latin-1")


def paginate():
    pages = []
    current = [(TITLE, 20, 0), (SUBTITLE, 11, 28), ("", 10, 20)]
    line_count = 3

    def add_line(text, size=10, gap=15):
        nonlocal current, line_count
        if line_count >= 43:
            pages.append(current)
            current = [(TITLE, 14, 0)]
            line_count = 1
        current.append((text, size, gap))
        line_count += 1

    for heading, questions in SECTIONS:
        add_line(heading, 14, 22)
        for question, answer in questions:
            add_line("Q: " + question, 11, 18)
            for wrapped in textwrap.wrap("A: " + answer, width=88):
                add_line(wrapped, 10, 14)
            add_line("", 10, 10)

    if current:
        pages.append(current)
    return pages


def build_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pages = paginate()
    objects = []

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = " ".join(f"{3 + index * 2} 0 R" for index in range(len(pages)))
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode("latin-1"))

    for index, lines in enumerate(pages):
        page_id = 3 + index * 2
        stream_id = page_id + 1
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> "
            f"/Contents {stream_id} 0 R >>".encode("latin-1")
        )
        stream = page_stream(lines)
        objects.append(b"<< /Length " + str(len(stream)).encode("latin-1") + b" >>\nstream\n" + stream + b"\nendstream")

    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode("latin-1"))
        output.extend(obj)
        output.extend(b"\nendobj\n")

    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    output.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("latin-1")
    )
    OUTPUT.write_bytes(output)


if __name__ == "__main__":
    build_pdf()
