"""
Colab utility functions - Host website in Colab and get public URL.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import os
from typing import Optional


def get_colab_website_url(website_path: str) -> Optional[str]:
    """
    Get a public URL for an HTML file in Google Colab.
    Uses ngrok tunneling for public access.

    Args:
        website_path: Path to the HTML file

    Returns:
        Public URL or None if not in Colab
    """
    try:
        from google.colab import files
        from google.colab.output import eval_js
        import subprocess

        website_path = Path(website_path)
        if not website_path.exists():
            print(f"❌ Website file not found: {website_path}")
            return None

        port = 8000
        os.system(f"cd {website_path.parent} && python -m http.server {port} > /dev/null 2>&1 &")

        subprocess.run(["pip", "install", "-q", "pyngrok"], capture_output=True)

        from pyngrok import ngrok
        ngrok.set_auth_token(os.environ.get("NGROK_AUTH_TOKEN", ""))

        public_url = ngrok.connect(port)
        file_url = f"{public_url}/files/browse/{website_path.name}"

        return str(public_url)

    except ImportError:
        print("ℹ️  Not running in Google Colab (use locally: open " + website_path + " in browser)")
        return None
    except Exception as e:
        print(f"⚠️ Could not generate public URL: {e}")
        return f"file://{Path(website_path).absolute()}"


def open_website_in_colab(website_path: str) -> str:
    """
    Display HTML website directly in Colab cell.

    Args:
        website_path: Path to the HTML file

    Returns:
        Display string or file path
    """
    try:
        from google.colab.output import IFrame
        website_path = Path(website_path)

        with open(website_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        return html_content
    except ImportError:
        return f"file://{Path(website_path).absolute()}"
    except Exception as e:
        print(f"Error: {e}")
        return None


def display_website_link(website_path: str) -> None:
    """
    Print both local and Colab-specific URLs.

    Args:
        website_path: Path to the HTML file
    """
    website_path = Path(website_path)

    if not website_path.exists():
        print(f"❌ Website file not found: {website_path}")
        return

    print(f"\n{'='*80}")
    print(f"📊 WEBSITE GENERATED SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"\n✓ Local Path: {website_path.absolute()}")
    print(f"\n📖 To view:")
    print(f"   • Windows/Mac/Linux: Double-click the HTML file")
    print(f"   • Terminal: open file://{website_path.absolute()}")

    colab_url = get_colab_website_url(str(website_path))
    if colab_url:
        print(f"\n🌐 Public Colab URL: {colab_url}")
    else:
        print(f"\n💡 For Colab access, run in cell:")
        print(f"   from src.utils.colab_utils import open_website_in_colab")
        print(f"   from IPython.display import HTML")
        print(f"   html = open_website_in_colab('{website_path}')")
        print(f"   display(HTML(html))")

    print(f"\n{'='*80}\n")
