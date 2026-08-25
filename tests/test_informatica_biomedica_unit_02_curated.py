from __future__ import annotations
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "informatica-biomedica" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "informatica-biomedica" / "unit-02.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "informatica-biomedica.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"
class InformaticaBiomedicaUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit=json.loads(SOURCE.read_text(encoding="utf-8")); cls.text=SOURCE.read_text(encoding="utf-8").casefold()
    def test_generated_unit_is_exact_redevelopment_mirror(self):
        self.assertEqual(SOURCE.read_bytes(),MIRROR.read_bytes())
    def test_identity_and_template_removal(self):
        self.assertEqual(self.unit["unit"],2); self.assertEqual(self.unit["slug"],"sistemas-de-informacion-clinica"); self.assertNotIn(GENERIC,self.text); self.assertNotIn("ppv=",self.text)
    def test_objectives_cover_systems_workflow_domains_and_downtime(self):
        t=" ".join(self.unit["learning_objectives"]).casefold()
        for p in ("ehr/his, cpoe, lis, ris, pacs","solicitud → aceptación/planificación → ejecución → resultado/informe → revisión","orden y espécimen","verificación farmacéutica, dispensación y administración","latencias y completitud de enlaces","downtime y recuperación"): self.assertIn(p,t)
    def test_five_substantive_theory_sections(self):
        s=self.unit["theory_sections"]; self.assertEqual(len(s),5)
        for x in s:
            self.assertGreaterEqual(len(x["paragraphs"]),6); self.assertGreaterEqual(len(x["key_points"]),6)
            for p in x["key_points"]: self.assertGreaterEqual(len(p.split()),5)
    def test_ehr_is_not_the_whole_hospital_system(self):
        t=json.dumps(self.unit["theory_sections"][0],ensure_ascii=False).casefold()
        for p in ("no es una única base de datos","no necesariamente ejecuta todas las tareas departamentales","identificador de paciente no sustituye al identificador de orden","el estado es parte del significado","u3 formalizará estándares de intercambio"): self.assertIn(p,t)
    def test_request_task_event_result_are_distinct(self):
        t=json.dumps(self.unit["theory_sections"][1],ensure_ascii=False).casefold()
        for p in ("una orden es una intención documentada","recursos de solicitud y recursos de evento","worklists","tiempo esperando","relaciones uno-a-muchos","resultado final no borra la historia"): self.assertIn(p,t)
    def test_lab_and_imaging_keep_domain_specific_objects(self):
        t=json.dumps(self.unit["theory_sections"][2],ensure_ascii=False).casefold()
        for p in ("órdenes, especímenes, pruebas, estados, resultados","fase preanalítica","ris, modalidades y pacs","identificador del estudio de imagen y el identificador del informe no son equivalentes","reconciliar identidad","no deben modelarse como idénticos"): self.assertIn(p,t)
    def test_medication_stages_are_separated(self):
        t=json.dumps(self.unit["theory_sections"][3],ensure_ascii=False).casefold()
        for p in ("medicationrequest","medicationdispense","medicationadministration","verificación farmacéutica no equivale a dispensación","dispensar tampoco prueba","no demuestra que el paciente haya recibido el medicamento"): self.assertIn(p,t)
    def test_metrics_do_not_claim_clinical_validity(self):
        sec=self.unit["theory_sections"][4]; t=json.dumps(sec,ensure_ascii=False).casefold()
        for p in ("tat=t_fin−t_inicio","c_enlace=n_enlazados/n_esperados","no demuestra que los enlaces sean correctos","downtime puede significar","reenviar todo sin control puede duplicar","disponibilidad alta no garantiza integridad ni seguridad"): self.assertIn(p,t)
        eq={x["latex"] for x in sec["equations"]}; self.assertIn(r"TAT=t_{fin}-t_{inicio}",eq); self.assertIn(r"C_{enlace}=\frac{N_{enlazados}}{N_{esperados}}",eq)
    def test_glossary_examples_and_activity_are_disciplinary(self):
        g={x["term"].casefold() for x in self.unit["glossary"]}; self.assertGreaterEqual(len(g),50)
        for p in ("ehr","cpoe","lis","ris","pacs","solicitud clínica","worklist","espécimen","estudio de imagen","informe radiológico","dispensación","administración","downtime","turnaround time","completitud de enlace","resultado huérfano"): self.assertIn(p,g)
        self.assertGreaterEqual(len(self.unit["worked_examples"]),5)
        a=self.unit["guided_activities"][0]; self.assertGreaterEqual(a["estimated_time_minutes"],300); self.assertGreaterEqual(len(a["problems"]),20); self.assertGreaterEqual(len(a["deliverables"]),12); self.assertGreaterEqual(len(a["checking_criteria"]),25)
    def test_common_errors_block_shortcuts(self):
        t=" ".join(x["error"]+" "+x["correction"] for x in self.unit["common_errors"]).casefold()
        for p in ("una orden implica ejecución","confundir ris y pacs","inferir exposición farmacológica","dispensación como administración","completitud de enlaces como exactitud","reenviar todo después de una interrupción"): self.assertIn(p,t)
    def test_sources_assessment_connections_and_notice(self):
        self.assertGreaterEqual(len(self.unit["sources"]),18); self.assertTrue(all(x["verification_status"]=="verified_directly" for x in self.unit["sources"])); self.assertGreaterEqual(len(self.unit["self_assessment"]),12); self.assertGreaterEqual(len(self.unit["biomedical_connections"]),6)
        n=self.unit["editorial_notice"].casefold()
        for p in ("exclusivamente","no constituye diseño ni validación","no deben introducirse datos identificables","implementación de estándares y terminologías se reserva para u3"): self.assertIn(p,n)
    def test_curricular_boundaries(self):
        p=self.unit["purpose"].casefold()
        for x in ("u3 queda reservada para interoperabilidad y terminologías","u4 para analítica","u5 para factores humanos","u6 para gobernanza e implementación"): self.assertIn(x,p)
    def test_published_descriptor_matches_canonical_purpose(self):
        subject=json.loads(SUBJECT.read_text(encoding="utf-8")); d={x["unit"]:x for x in subject["detailed_units"]}
        self.assertEqual(d[2]["description"],self.unit["purpose"])
if __name__=="__main__":
    unittest.main()
