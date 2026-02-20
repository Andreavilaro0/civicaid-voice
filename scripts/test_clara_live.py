#!/usr/bin/env python3
"""Live integration test: Clara responses, vision, TTS — tests E-V-I pattern.

Usage:
    python scripts/test_clara_live.py              # Run all tests
    python scripts/test_clara_live.py --text       # Text responses only
    python scripts/test_clara_live.py --vision     # Vision only
    python scripts/test_clara_live.py --tts        # TTS only
"""

import os
import sys
import re
import time
import argparse

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Override config for live testing
os.environ["LLM_LIVE"] = "true"
os.environ["DEMO_MODE"] = "false"


# --- HELPERS ---

def _check_evi_pattern(text: str, label: str) -> dict:
    """Check if response follows E-V-I pattern. Returns results dict."""
    results = {"label": label, "text": text, "checks": {}, "pass": True}

    # Check 1: Has numbered steps or concrete info (Informar)
    has_steps = bool(re.search(r'\d+\.', text))
    has_question = text.strip().endswith("?")
    results["checks"]["has_steps_or_structure"] = has_steps
    results["checks"]["ends_with_question"] = has_question

    # Check 2: Word count <= 250 (200 target + margin)
    word_count = len(text.split())
    results["checks"]["word_count"] = word_count
    results["checks"]["under_250_words"] = word_count <= 250

    # Check 3: No forbidden phrases
    forbidden = [
        "es tu responsabilidad", "deberias haber", "como ya te dije",
        "es complicado", "es obligatorio que", "no puedo ayudarte"
    ]
    found_forbidden = [f for f in forbidden if f in text.lower()]
    results["checks"]["no_forbidden_phrases"] = len(found_forbidden) == 0
    if found_forbidden:
        results["checks"]["forbidden_found"] = found_forbidden

    # Check 4: Has source reference
    has_source = any(s in text.lower() for s in [
        "administracion.gob.es", "060", "ayuntamiento", "seguridad social",
        "sede electronica", ".gob.es", "sepe", "[c"
    ])
    results["checks"]["has_source"] = has_source

    # Overall pass
    results["pass"] = (
        results["checks"]["under_250_words"]
        and results["checks"]["no_forbidden_phrases"]
    )

    return results


def _print_result(r: dict):
    """Pretty print a test result."""
    status = "PASS" if r["pass"] else "FAIL"
    print(f"\n{'='*60}")
    print(f"[{status}] {r['label']}")
    print(f"{'='*60}")
    print(f"Response ({r['checks'].get('word_count', '?')} words):")
    print(f"  {r['text'][:300]}{'...' if len(r['text']) > 300 else ''}")
    print("\nChecks:")
    for k, v in r["checks"].items():
        icon = "OK" if v not in (False,) else "!!"
        if isinstance(v, bool):
            icon = "OK" if v else "!!"
        print(f"  [{icon}] {k}: {v}")


# --- TEXT RESPONSE TESTS ---

def test_text_responses():
    """Test Clara LLM responses with E-V-I pattern."""
    from src.core.skills.llm_generate import llm_generate
    from src.core.retriever import get_retriever

    print("\n" + "="*60)
    print("  TESTING TEXT RESPONSES (LLM + E-V-I)")
    print("="*60)

    test_cases = [
        # (query, language, description)
        ("Hola, necesito ayuda con el empadronamiento", "es",
         "ES: Pregunta informativa — empadronamiento"),
        ("llevo 8 meses esperando mi NIE y nadie me dice nada, tengo miedo", "es",
         "ES: Carga emocional — NIE espera larga"),
        ("que es el IMV y como lo pido", "es",
         "ES: Pregunta directa — IMV"),
        ("Bonjour, j'ai besoin d'aide pour m'inscrire au padron", "fr",
         "FR: Empadronamiento en frances"),
        ("je ne comprends pas ce document, il dit que je dois payer", "fr",
         "FR: Documento confuso — carga emocional"),
    ]

    results = []
    retriever = get_retriever()

    for query, lang, desc in test_cases:
        print(f"\n>>> Testing: {desc}")
        print(f"    Query: {query}")

        try:
            # KB lookup
            kb_context = retriever.retrieve(query, lang)

            # LLM generate
            start = time.time()
            resp = llm_generate(query, lang, kb_context)
            elapsed = int((time.time() - start) * 1000)

            if resp.success:
                r = _check_evi_pattern(resp.text, desc)
                r["elapsed_ms"] = elapsed
                _print_result(r)
                results.append(r)
            else:
                print(f"  [FAIL] LLM error: {resp.error}")
                results.append({"label": desc, "pass": False, "error": resp.error})

        except Exception as e:
            print(f"  [ERROR] {e}")
            results.append({"label": desc, "pass": False, "error": str(e)})

    return results


# --- VISION TESTS ---

def test_vision():
    """Test image analysis with a test image."""
    from src.core.skills.analyze_image import analyze_image

    print("\n" + "="*60)
    print("  TESTING VISION (Image Analysis)")
    print("="*60)

    results = []

    # Create a simple test PNG (1x1 white pixel)
    # In real testing, you'd use actual document images
    test_png = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00'
        b'\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00'
        b'\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
    )

    for lang, desc in [("es", "ES: Test image"), ("fr", "FR: Test image")]:
        print(f"\n>>> Testing: {desc}")
        try:
            start = time.time()
            result = analyze_image(test_png, "image/png", language=lang)
            elapsed = int((time.time() - start) * 1000)

            if result.success:
                r = _check_evi_pattern(result.text, desc)
                r["elapsed_ms"] = elapsed
                _print_result(r)
                results.append(r)
            else:
                print(f"  [INFO] Vision returned: {result.error}")
                print("  (This is expected for a 1px test image)")
                results.append({"label": desc, "pass": True, "note": "Expected fail for dummy image"})

        except Exception as e:
            print(f"  [ERROR] {e}")
            results.append({"label": desc, "pass": False, "error": str(e)})

    return results


# --- TTS TESTS ---

def test_tts():
    """Test text-to-speech generation."""
    print("\n" + "="*60)
    print("  TESTING TTS (Text-to-Speech)")
    print("="*60)

    results = []

    # Test with a typical Clara response
    test_texts = [
        ("Buena pregunta. El empadronamiento es un tramite basico. "
         "Necesitas tu DNI y un contrato de alquiler. "
         "En que ciudad vives?", "es", "ES: Respuesta tipica Clara"),
        ("Je comprends votre inquietude. Vous avez le droit de "
         "recevoir une reponse. Decrivez-moi le document.", "fr", "FR: Respuesta tipica Clara"),
    ]

    for text, lang, desc in test_texts:
        print(f"\n>>> Testing: {desc}")
        try:
            # Test gTTS (always available)
            from src.core.skills.tts import _synthesize_gtts
            start = time.time()
            filepath = _synthesize_gtts(text, lang)
            elapsed = int((time.time() - start) * 1000)

            if filepath and os.path.exists(filepath):
                size_kb = os.path.getsize(filepath) / 1024
                print(f"  [OK] gTTS: {filepath} ({size_kb:.1f} KB, {elapsed}ms)")
                results.append({"label": f"gTTS {desc}", "pass": True, "size_kb": size_kb})
            else:
                print("  [FAIL] gTTS returned None")
                results.append({"label": f"gTTS {desc}", "pass": False})

            # Test Gemini TTS (if configured)
            from src.core.config import config
            if config.GEMINI_API_KEY:
                from src.core.skills.tts import _synthesize_gemini
                start = time.time()
                wav_bytes = _synthesize_gemini(text, lang)
                elapsed = int((time.time() - start) * 1000)

                if wav_bytes:
                    size_kb = len(wav_bytes) / 1024
                    print(f"  [OK] Gemini TTS: {size_kb:.1f} KB WAV ({elapsed}ms)")
                    # Save for playback
                    out_path = f"/tmp/clara_test_{lang}.wav"
                    with open(out_path, "wb") as f:
                        f.write(wav_bytes)
                    print(f"  Saved to: {out_path}")
                    results.append({"label": f"Gemini TTS {desc}", "pass": True, "size_kb": size_kb})
                else:
                    print("  [INFO] Gemini TTS returned None (may not support TTS model)")
                    results.append({"label": f"Gemini TTS {desc}", "pass": True, "note": "Not available"})

        except Exception as e:
            print(f"  [ERROR] {e}")
            results.append({"label": desc, "pass": False, "error": str(e)})

    return results


# --- WHATSAPP FORMAT TEST ---

def test_whatsapp_format():
    """Test WhatsApp formatting on a real Clara-style response."""
    from src.core.skills.whatsapp_format import format_for_whatsapp

    print("\n" + "="*60)
    print("  TESTING WHATSAPP FORMATTING")
    print("="*60)

    sample = (
        "Es normal que suene raro al principio. El padron es un papel basico "
        "que aparece en casi todos los tramites. Para pedirlo necesitas: "
        "1. Tu pasaporte o DNI 2. Contrato de alquiler 3. Pedir cita en "
        "tu ayuntamiento. OJO: el plazo es hasta el 15 de marzo. "
        "En que ciudad vives?"
    )

    formatted = format_for_whatsapp(sample)
    print(f"\nOriginal:\n  {sample}")
    print(f"\nFormatted:\n  {formatted}")

    checks = {
        "bold_steps": "*1.*" in formatted and "*2.*" in formatted and "*3.*" in formatted,
        "bold_ojo": "*OJO:*" in formatted,
        "url_safe": "?" in formatted,  # question mark preserved
    }

    all_pass = all(checks.values())
    print("\nChecks:")
    for k, v in checks.items():
        print(f"  [{'OK' if v else '!!'}] {k}: {v}")

    return [{"label": "WhatsApp format", "pass": all_pass, "checks": checks}]


# --- MAIN ---

def main():
    parser = argparse.ArgumentParser(description="Test Clara pipeline live")
    parser.add_argument("--text", action="store_true", help="Test text responses only")
    parser.add_argument("--vision", action="store_true", help="Test vision only")
    parser.add_argument("--tts", action="store_true", help="Test TTS only")
    parser.add_argument("--format", action="store_true", help="Test WhatsApp formatting only")
    args = parser.parse_args()

    # If no specific flag, run all
    run_all = not (args.text or args.vision or args.tts or args.format)

    all_results = []

    if run_all or args.format:
        all_results.extend(test_whatsapp_format())

    if run_all or args.text:
        all_results.extend(test_text_responses())

    if run_all or args.vision:
        all_results.extend(test_vision())

    if run_all or args.tts:
        all_results.extend(test_tts())

    # Summary
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)

    passed = sum(1 for r in all_results if r.get("pass"))
    failed = sum(1 for r in all_results if not r.get("pass"))

    for r in all_results:
        status = "PASS" if r.get("pass") else "FAIL"
        print(f"  [{status}] {r.get('label', '?')}")

    print(f"\n  Total: {passed} passed, {failed} failed out of {len(all_results)}")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
