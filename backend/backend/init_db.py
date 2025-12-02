from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

sample_videos = [
    models.Video(title="감동적인 사연 - 남편의 진심", url="https://youtu.be/example1"),
    models.Video(title="충격적인 고백 - 시어머니의 비밀", url="https://youtu.be/example2"),
    models.Video(title="눈물 나는 이야기 - 20년의 결혼생활", url="https://youtu.be/example3"),
]

db.add_all(sample_videos)
db.commit()
db.close()
