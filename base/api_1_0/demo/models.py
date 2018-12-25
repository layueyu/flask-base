
from base import db_
from base.api_1_0.base.base import BaseModel


# 建立Demo1与Demo的多对多关系
demo_demo1 = db_.Table(
    "tb_demo_demo1",
    db_.Column("demo_id", db_.Integer, db_.ForeignKey("tb_demo.id"), primary_key=True),  # demo编号
    db_.Column("demo1_id", db_.Integer, db_.ForeignKey("tb_demo1.id"), primary_key=True)  # demo1编号
)


class Demo(BaseModel, db_.Model):
    __tablename__ = "tb_demo"

    id = db_.Column(db_.Integer, primary_key=True)  # 房屋编号
    address = db_.Column(db_.String(512), default="")  # 地址
    facilities = db_.relationship("Demo1", secondary=demo_demo1)  # 房屋的设施


class Demo1(BaseModel, db_.Model):
    __tablename__ = "tb_demo1"

    id = db_.Column(db_.Integer, primary_key=True)  # 编号
    name = db_.Column(db_.String(512), default="")  # 名称
