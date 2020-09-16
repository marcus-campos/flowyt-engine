class WorkerFrequency:
    def __init__(self, session):
        self.session = session()

    def get_or_create(self, model, worker_name):
        result = self.session.query(model).filter_by(worker_name=worker_name).first()

        if result:
            return result
        else:
            result = model(worker_name=worker_name)
            self.session.add(result)
            self.session.commit()
            return result