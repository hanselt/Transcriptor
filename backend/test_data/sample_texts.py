TEST_CASES = [
    {
        "input": "Hola esto es una prueba del sistema",
        "min_length": 10,
        "expected_lang": "es",
        "expected_keywords": ["prueba", "sistema"]
    },
    {
        "input": "The quick brown fox jumps",
        "min_length": 8,
        "expected_lang": "en",
        "expected_keywords": ["fox", "jumps"]
    },
    {
        "input": "Short",  # Caso mínimo
        "min_length": 1,
        "expected_lang": "en",
        "expected_keywords": []
    }
]

def validate_output(output: dict, test_case: dict) -> bool:
    """Función de validación personalizada"""
    if len(output["text"]) < test_case["min_length"]:
        return False
    if output["language"] != test_case["expected_lang"]:
        return False
    for keyword in test_case["expected_keywords"]:
        if keyword.lower() not in output["text"].lower():
            return False
    return True