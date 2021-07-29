import json
import re
from pathlib import Path
from yargy import Parser, rule, or_, and_, not_
from yargy.predicates import eq, normalized, type, is_upper
from yargy.interpretation import fact
from yargy.tokenizer import TokenRule
from dictionaries import OpenCorpora

Document = fact('Document', ['type', 'number_sign', 'number_value', 'second_number'])

opencorpora = OpenCorpora()

WORD = not_(eq('*')).optional()

LEFT_BRACKET = or_(rule('('), rule('['), rule('{'))
RIGHT_BRACKET = or_(rule('}'), rule(')'), rule('}'))
INT = type('INT')
LATIN = type('LATIN')
DASH = eq('-')
RU = type('RU')
LATIN_ABBR = rule(and_(LATIN, is_upper()))
RU_ABBR = rule(and_(RU, is_upper()))

NUMBER_VALUE = rule(or_(rule(LATIN_ABBR), rule(RU_ABBR), rule(INT), rule(DASH))).repeatable().interpretation(Document.number_value)

NOMER = or_(rule(normalized('номер')),
            rule('N'),
            rule('№'),
            rule('#')).interpretation(Document.number_sign)

MTS = or_(rule('М', 'Т', 'С'),
          rule('МТС')).interpretation(Document.type)
AKT = or_(rule(normalized('акт')),
          rule('А', 'К', 'Т')).interpretation(Document.type.normalized())
DOGOVOR = rule(normalized('договор')).interpretation(Document.type.normalized())
ZAKAZ = rule(normalized('заказ')).interpretation(Document.type.normalized())

NUMBER_BRACKETS = rule(
    or_(rule('('), rule('{'), rule('[')),
    or_(
        rule(LATIN_ABBR),
        rule(RU_ABBR),
        rule(INT),
        rule(DASH)).repeatable(),
    or_(rule(')'), rule('}'), rule(']'))
    ).interpretation(Document.second_number)

NOMER_MTS = rule(or_(rule(NOMER, MTS, NUMBER_VALUE), rule(MTS, ':', NUMBER_VALUE))).interpretation(Document)
NOMER_AKTA = rule(AKT, NOMER, NUMBER_VALUE, NUMBER_BRACKETS.optional()).interpretation(Document)
NOMER_DOGOVORA = rule(DOGOVOR, NOMER, NUMBER_VALUE, NUMBER_BRACKETS.optional()).interpretation(Document)
NOMER_ZAKAZA = rule(ZAKAZ, NOMER, NUMBER_VALUE, NUMBER_BRACKETS.optional()).interpretation(Document)

data_path = 'data/acts.json'

OrderParser = Parser(NOMER_ZAKAZA)
ActsParser = Parser(NOMER_AKTA)
MTSParser = Parser(NOMER_MTS)
ContractParser = Parser(NOMER_DOGOVORA)

