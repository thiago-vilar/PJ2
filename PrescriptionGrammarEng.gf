-- PrescriptionGrammarEng.gf
concrete PrescriptionGrammarEng of PrescriptionGrammar = PrescriptionLexiconEng ** {
  lincat
    Command = Str ;
    Instruction = Str ;
    BodyPart = Str ; 

  lin
    Prescribe instr = "Prescribe:" ++ instr ;
    Take med dose unit freq = "Take" ++ dose ++ unit ++ "of" ++ med ++ freq ;
    Apply dose unit part freq = "Apply" ++ dose ++ unit ++ "to the" ++ part ++ freq ; -- Adiciona a função Apply.
}
