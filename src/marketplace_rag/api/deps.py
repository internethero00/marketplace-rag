from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from marketplace_rag.db.session import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
