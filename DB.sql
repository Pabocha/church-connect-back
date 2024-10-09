CREATE TABLE Membres(
    id_membre INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL,
    email VARCHAR(60),
    numero_tel VARCHAR(30),
    profession VARCHAR(255),
    image_ IMAGE(),
    -- status_()
    date_save DATETIME,
)

CREATE TABLE Programmes(
    id_programme_eglise INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(255) NOT NULL,
    message_ TEXT,
    heure_debut TIMESTAMP,
    heure_fin TIMESTAMP,
)

CREATE TABLE Annonces(
    id_programme_special INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(255) NOT NULL,
    message_ TEXT,
    lieu VARCHAR(255),
    date_annonce DATETIME,
    date_annonce_second DATETIME,
    date_create DATETIME NOT NULL,
)

CREATE TABLE ProgrammeSpecial(
    frequence_choices {
        'jours', 'tous les jours',
        'semaines', 'toutes les semaines',
        'mois', 'tous les mois'
    }
    list_day_for_weeks_choices{
        'Lun', 'Lundi',
        'Mar', 'Mardi',
        'Mer', 'Mercredi',
        'Jeu', 'Jeudi',
        'Ven', 'Vendredi',
        'Sam', 'Samedi',
        'Dim', 'Dimanche',
    }
    repete_envent_choices {
        'Toujours', 'Toujours',
        "until", "jusqu'à une certaine date"
    }
    repete_month_choices {
        'same', 'Le même jour chaque mois'
        'first_day', 'Tous les premiers jours du jour choisi'
    }

    id_programme_eglise INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(255) NOT NULL,
    message_ TEXT,
    heure_debut TIMESTAMP,
    heure_fin TIMESTAMP,
    date_debut DATE,
    date_fin DATE,
    frequence VARCHAR(choices=frequence_choices),
    list_day_for_weeks = VARCHAR(choices=list_day_for_weeks_choices),
    repete_envent VARCHAR(choices=repete_envent_choices),
    date_until = DATE,
    repete_month = VARCHAR(choices=)
)