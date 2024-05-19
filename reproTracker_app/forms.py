from django import forms
from .models import *

class PersonneForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['nom', 'prenom', 'date_naiss', 'cin', 'nationalite', 'adress', 'ville', 'metier', 'etat_civil', 'sexe']

class PratiqueForm(forms.ModelForm):
    class Meta:
        model = Pratique
        fields = ['connaissance', 'cle_conn', 'consultation', 'question']


class IstForm(forms.ModelForm):
    class Meta:
        model = Ist
        fields = ['vih_sid', 'syphilis', 'gonorrhee', 'chlamydiose', 'trichomonase', 'hepatite_b', 'hsv', 'pvh', 'taux_depistoge']


class PrenatalMaternelForm(forms.ModelForm):
    class Meta:
        model = PrenatalMaternel
        fields = ['acc_serv_prenatal', 'comp_grass', 'desc_comp_gross', 'comp_accouch', 'desc_comp_accouch', 'acc_serv_maternel', 'meth_accouch']


class SrForm(forms.ModelForm):
    class Meta:
        model = Sr
        fields = ['nb_verification_sr', 'acc_service_examen', 'problemes_sex', 'qualité_relation_sex', 'demande_soutien']

class ViolenceForm(forms.ModelForm):
    class Meta:
        model = Violence
        fields = ['taux_viol_sex', 'agress_sex', 'taux_abus_viol_sex', 'soutien_psyc', 'type_harcelement_sex', 'taux_harcelement_sex']


class GrossesseForm(forms.ModelForm):
    class Meta:
        model = Grossesse
        fields = ['planification', 'meth_planification', 'envi_enfant', 'nb_enfant', 'nb_enfant_planifie', 'nb_enfant_nplanifie', 'nb_fausse_couche', 'nb_fausse_couche_intentionnelle', 'nb_enfant_hors_mariage']

class FacteurForm(forms.ModelForm):
    class Meta:
        model = Facteur
        fields = ['religion', 'niv_etud', 'revenu', 'niv_social', 'impact_norme_culturelle', 'impact_norme_religieuse']
