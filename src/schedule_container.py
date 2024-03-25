from config import mongodb
from pymongo import MongoClient
from redis import StrictRedis
from dependency_injector import containers, providers
from config import redis
from domain.schedule.dao.bus_schedule_dao import MongoDBBusScheduleDao
from domain.schedule.dao.train_schedule_dao import ExternalTrainScheduleDao
from domain.schedule.dao.train_schedule_cacher import RedisTrainScheduleCacher
from domain.schedule.service.schedule_query_service import ScheduleQueryService


class ScheduleContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.schedule'])

    mongodb_connection = providers.Singleton(MongoClient, host=mongodb.host, username=mongodb.username, password=mongodb.password, port=mongodb.port)
    redis_connection = providers.Singleton(
        StrictRedis,
        host=redis.host,
        port=redis.port,
        password=redis.pwd,
        decode_responses=True
    )

    train_schedule_dao = providers.Singleton(ExternalTrainScheduleDao)
    train_schedule_cacher = providers.Singleton(RedisTrainScheduleCacher, redis_connection=redis_connection)
    bus_schedule_dao = providers.Singleton(MongoDBBusScheduleDao, connection=mongodb_connection)

    schedule_query_service = providers.Singleton(ScheduleQueryService,
                                                 bus_schedule_dao=bus_schedule_dao,
                                                 train_schedule_dao=train_schedule_dao,
                                                 train_schedule_cacher=train_schedule_cacher)
