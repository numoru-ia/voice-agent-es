"""Function-calling tools exposed to the LLM."""

def load_tools(tenant_id: str):
    return [
        {
            "type": "function",
            "function": {
                "name": "search_clinic_info",
                "description": "Busca información (servicios, precios, horarios, FAQs) en el RAG de la clínica.",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "find_available_slot",
                "description": "Encuentra horario disponible.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service_id": {"type": "string"},
                        "from_date": {"type": "string"},
                        "preferred_time": {"type": "string", "enum": ["morning", "afternoon", "any"]},
                    },
                    "required": ["service_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "book_appointment",
                "description": "Agenda una cita confirmada.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_phone": {"type": "string"},
                        "patient_name": {"type": "string"},
                        "slot_id": {"type": "string"},
                    },
                    "required": ["patient_phone", "patient_name", "slot_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "transfer_to_human",
                "description": "Transfiere a recepcionista humana.",
                "parameters": {
                    "type": "object",
                    "properties": {"reason": {"type": "string"}},
                },
            },
        },
    ]
