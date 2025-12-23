def load_model(model_name):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        logger.info(f"Model '{model_name}' loaded successfully.")
        return model, tokenizer
    except Exception as e:
        logger.error(f"Error loading model '{model_name}': {e}")
        return None, None