abstract PrescriptionLexicon = {
  flags startcat = Medication ;

  cat
    Medication ;  -- Medicamentos
    Unit ;        -- Unidades de medida
    Dosage ;      -- Doses
    Frequency ;   -- Frequência
    BodyPart ;    -- Partes do corpo

  fun
    Aspirin : Medication ;
    Tablet : Unit ;
    Drop : Unit ;
    OnceADay : Frequency ;
    TwiceADay : Frequency ;
    One : Dosage ;
    Two : Dosage ;
    AffectedEye : BodyPart ; 
}
