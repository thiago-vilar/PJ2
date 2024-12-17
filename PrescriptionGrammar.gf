abstract PrescriptionGrammar = PrescriptionLexicon ** {
  flags startcat = Command ;

  cat
    Command ;      -- Comandos de prescrição
    Instruction ;  -- Instrução principal
    BodyPart ;     -- Partes do corpo 

  fun
    Prescribe : Instruction -> Command ;
    Take : Medication -> Dosage -> Unit -> Frequency -> Instruction ;
    Apply : Dosage -> Unit -> BodyPart -> Frequency -> Instruction ;
}
