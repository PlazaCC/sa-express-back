from datetime import datetime

def now_timestamp() -> str:
    return str(int(datetime.now().timestamp() * 1000))

def error_with_instruction_sufix(error: str, instr_index: int):
    return error + f' at instruction {str(instr_index)}'