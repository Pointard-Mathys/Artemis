from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import Table, Column, Integer, ForeignKey

import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/callcountdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#______________________________________________________test echo


class CallCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)

@app.route('/get_echo', methods=['GET'])
def get_echo():
    try:
        call_count = CallCount.query.get(1)
        if call_count is None:
            call_count = CallCount(id=1, count=0)

        call_count.count += 20
        db.session.add(call_count)
        db.session.commit()

        return jsonify({'message': {'content':'Echo', 'count': call_count.count}})
    except OperationalError:
        return jsonify({'error': 'Database connection error'}), 500



#______________________________________________________création class agent + création agent
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # dispo = db.Column(db.Integer, nullable=False)
    dispo = db.Column(db.Boolean, nullable=False, default=True)  # Champ pour suivre la disponibilité de l'agent


@app.route('/new_agent', methods=['GET'])
def new_agent():
    try:
        #nous partont du constat que nous somme dans une caserne de volontaire la dipos du pompier et aléatoire en fontion de lui. 1= dispo 0=indispo
        new_agent = Agent(dispo=random.choice([True, False]))
        db.session.add(new_agent)
        db.session.commit()

        return jsonify({'message': {'content': 'New agent created', 'dispo': new_agent.dispo}})
    except OperationalError:
        return jsonify({'error': 'Database connection error'}), 500



#______________________________________________________création class véhicule + création véhicule CCR et VSAV

class Vehicule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    nb_agent = db.Column(db.Integer, nullable=False)


@app.route('/vehicule', methods=['GET'])
def create_vehicules():
    try:
        #VSAV = véhicule de secours et d'assistance aux victimes
        vsav = Vehicule.query.filter_by(name='VSAV').first()
        #CCR =  Camion Citerne Rural
        ccr = Vehicule.query.filter_by(name='CCR').first()

        if vsav is None:
            vsav = Vehicule(name='VSAV', nb_agent = 4)
            db.session.add(vsav)

        if ccr is None:
            ccr = Vehicule(name='CCR', nb_agent = 6)
            db.session.add(ccr)

        db.session.commit()

        return jsonify({'message': 'Vehicules created successfully'})
    except OperationalError:
        return jsonify({'error': 'Database connection error'}), 500
    
    
    
    
    
#______________________________________________________création class intervention + création intervention
# Définition de la table de liaison entre Agent et Intervention
agent_intervention = Table(
    'agent_intervention', db.Model.metadata,
    Column('agent_id', Integer, ForeignKey('agent.id')),
    Column('intervention_id', Integer, ForeignKey('intervention.id'))
)




class Intervention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #on peut avoir deux type d'intervention classique
    type = db.Column(db.String(50), nullable=False)
    # #id du véhicule prit
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicule.id'), nullable=True)
    # #relation a la table véhicule
    vehicle = db.relationship('Vehicule', backref='interventions', lazy=True)
    # #relation a la table agent
    agents = db.relationship('Agent', secondary=agent_intervention, backref='interventions',
                             lazy='dynamic',  # Changer la stratégie de chargement à dynamique
                             primaryjoin="Intervention.id == agent_intervention.c.intervention_id")


@app.route('/new_intervention', methods=['GET'])
def new_intervention():
    try:
        intervention_type = random.choice(["feu de maison", "malaise"])
        
        # Sélectionner un véhicule en fonction du type d'intervention
        if intervention_type == "feu de maison":
            vehicle = Vehicule.query.filter_by(name="CCR").first()
        elif intervention_type == "malaise":
            vehicle = Vehicule.query.filter_by(name="VSAV").first()
        else:
            # Gérer d'autres types d'intervention si nécessaire
            return jsonify({'error': 'Unknown intervention type'}), 400
        
        # Créer la nouvelle intervention avec le véhicule sélectionné
        new_intervention = Intervention(type=intervention_type, vehicle=vehicle)
        db.session.add(new_intervention)
        db.session.commit()
        
# Vérifier si le véhicule a suffisamment d'agents disponibles
        if vehicle.nb_agent > 0:
            # Sélectionner les agents disponibles en fonction du nombre requis pour le véhicule
            available_agents = Agent.query.filter_by(dispo=True).limit(vehicle.nb_agent).all()
            
            # Si suffisamment d'agents sont disponibles, les attribuer à l'intervention
            if len(available_agents) == vehicle.nb_agent:
                new_intervention = Intervention(type=intervention_type, vehicle=vehicle)
                db.session.add(new_intervention)
                for agent in available_agents:
                    new_intervention.agents.append(agent)
                    agent.dispo = False  # Mettre jour la disponibilité de l'agent
                db.session.commit()
                
                return jsonify({'message': {'content': 'New intervention created', 'type': intervention_type, 'vehicle_id': vehicle.id, 'agents_assigned': len(available_agents)}})
            else:
                return jsonify({'error': 'Not enough available agents for this intervention'}), 400
        else:
            return jsonify({'error': 'No agents available for this vehicle'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500




#_____________________________________________________serveur

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
