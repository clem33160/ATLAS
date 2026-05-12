from dataclasses import dataclass
@dataclass
class Invoice: id:str; amount:float; paid:bool=False
