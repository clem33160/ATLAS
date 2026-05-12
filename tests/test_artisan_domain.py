from core.artisan.followup import unpaid_invoices
from core.artisan.invoice import Invoice

def test_unpaid_followup():
    assert len(unpaid_invoices([Invoice('1',10,False), Invoice('2',10,True)]))==1
