import datetime 
from sqlalchemy import String, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    entries: Mapped[list["HabitEntry"]] = relationship(
        back_populates="habit",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class HabitEntry(Base):
    __tablename__ = "habit_entries"

    __table_args__ = (
        UniqueConstraint("habit_id", "date", name="uq_habit_entry_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id", ondelete="CASCADE")
    )
    date: Mapped[datetime.date] = mapped_column()

    habit: Mapped["Habit"] = relationship(
        back_populates="entries"
    )