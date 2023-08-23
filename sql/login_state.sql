DROP TABLE IF EXISTS login_state;
CREATE TABLE login_state(
    `id` BIGINT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    `uid` VARCHAR(255) NOT NULL   COMMENT 'UID' ,
    `credential` VARCHAR(255) NOT NULL   COMMENT '登录的凭证' ,
    PRIMARY KEY (id)
)  COMMENT = '登录状态记录表';
