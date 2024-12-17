concrete PrescriptionGrammarBra of PrescriptionGrammar = PrescriptionLexiconBra ** {
  lincat
    Command = Str ;
    Instruction = Str ;
    BodyPart = Str ;

  lin
    Prescribe instr = "Prescreva:" ++ instr ;
    Take med dose unit freq = "Tomar" ++ dose ++ unit ++ "de" ++ med ++ freq ;
    Apply dose unit part freq = "Aplicar" ++ dose ++ unit ++ "no" ++ part ++ freq ;
}
