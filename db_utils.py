from pathlib import Path
from typing import Dict, List

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from sqlite3 import IntegrityError

# db_models
class Base(DeclarativeBase):
    pass

class Probeset(Base):
    __tablename__ = "probeset"
    id: Mapped[str] = mapped_column(primary_key=True)
    num_probes: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Probeset(id:{self.id}, num_probes:{self.num_probes})"

class Transcript(Base):
    __tablename__ = "transcript"
    id: Mapped[str] = mapped_column(primary_key=True)
    gene_id: Mapped[str] = mapped_column()
    gene_name: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Transcript(id:{self.id}, gene_id:{self.gene_id}, gene_name:{self.gene_name})"

class ProbesetTranscript(Base):
    # join table
    __tablename__ = "probeset_transcript"
    probeset_id: Mapped[str] = mapped_column(ForeignKey("probeset.id"), primary_key=True)
    transcript_id: Mapped[str] = mapped_column(ForeignKey("transcript.id"), primary_key=True)

    def __repr__(self) -> str:
        return f"ProbeTranscript(probeset_id:{self.probeset_id}, transcript_id:{self.transcript_id})"

def create_sqlitedb_if_not_exists(db_filename: str = "probesets.db") -> Engine:
    db_path: Path = Path(db_filename)
    engine: Engine = create_engine(f"sqlite:///{db_filename}", echo=True)
    if not db_path.is_file():
        Base.metadata.create_all(engine) # creates the db and all the tables
    return engine

def load_probeset_response_jsons(engine: Engine, probeset_response_jsons: List[Dict]) -> None:
    with Session(engine) as session:
        probesets: List = []
        transcripts: List = []
        probesets_transcripts: List = []
        for probeset_response_json in probeset_response_jsons:
            probesets.append(Probeset(
                id = probeset_response_json["name"],
                num_probes = probeset_response_json["size"]
            ))
            for transcript in probeset_response_json["transcripts"]:
                transcripts.append(Transcript(
                    id = transcript["stable_id"],
                    gene_id = transcript["gene"]["stable_id"],
                    gene_name = transcript["gene"]["external_name"]
                ))
                probesets_transcripts.append(ProbesetTranscript(
                    probeset_id = probeset_response_json["name"],
                    transcript_id = transcript["stable_id"]
                ))

        # TODO: ditch all this try/except and switch to get-by-primarykey and then add
        # for each record:
        # see: https://docs.sqlalchemy.org/en/20/orm/session_basics.html#get-by-primary-key

        try:
            session.add_all(probesets)
        except IntegrityError:
            session.rollback()
        except:
            session.rollback()
            raise

        try:
            session.add_all(transcripts)
        except IntegrityError:
            session.rollback()
        except:
            session.rollback()
            raise

        try:
            session.add_all(probesets_transcripts)
        except IntegrityError:
            session.rollback()
        except:
            session.rollback()
            raise

        session.commit()
