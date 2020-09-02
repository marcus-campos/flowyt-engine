class Contracts:
    def __init__(self, session):
        self.session = session()

    def get_or_create(self, model, contract, description, short_description):
        result = self.session.query(model).filter_by(contract=contract).first()

        if result:
            return result
        else:
            result = model(contract=contract, description=description, short_description=short_description)
            self.session.add(result)
            self.session.commit()
            return result


class Vulnerabilities:
    def __init__(self, session):
        self.session = session()

    def get_or_create(self, model, name):
        result = self.session.query(model).filter_by(name=name).first()

        if result:
            return result
        else:
            result = model(name=name)
            self.session.add(result)
            self.session.commit()
            return result


class VulnerabilitiesCount:
    def __init__(self, session):
        self.session = session()

    def get_or_create(self, models, vuln_name, contract_number, total):
        vuln_count_model = models.VulnerabilitiesCount
        vuln_model = models.Vulnerabilities
        contract_model = models.Contracts

        contract = self.session.query(contract_model).filter_by(contract=contract_number).first()
        vuln = self.session.query(vuln_model).filter_by(name=vuln_name).first()

        if not (contract and vuln):
            return False
        
        result = vuln_count_model(contract_id=str(contract.id), total=total, vulnerability_id=str(vuln.id))
        self.session.add(result)
        self.session.commit()
        return result