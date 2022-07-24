from fastapi import FastAPI, Depends
from sqlalchemy.sql import Select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from connections.database import init_db
from models import Bet
from connections.database import get_session


app = FastAPI(
    title='Bet Maker'
)


@app.on_event('startup')
async def startup():
    await init_db()


@app.get('/bets', response_model=list[Bet])
async def get_bets(session: AsyncSession = Depends(get_session)):
    expr: Select = select(Bet)
    result = (await session.exec(expr)).all()
    return result


@app.post('/bets', response_model=Bet)
async def create_bet(bet: Bet, session: AsyncSession = Depends(get_session)):
    session.add(bet)
    await session.commit()
    await session.refresh(bet)
    return bet

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)