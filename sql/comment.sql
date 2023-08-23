DROP TABLE IF EXISTS comment;
CREATE TABLE comment(
    `id` BIGINT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    `bid` VARCHAR(255) NOT NULL   COMMENT '视频BV号' ,
    `cid` BIGINT NOT NULL   COMMENT 'B站评论ID' ,
    `uid` BIGINT NOT NULL   COMMENT '用户UID' ,
    `uname` VARCHAR(255) NOT NULL   COMMENT 'B站用户名' ,
    `message` VARCHAR(255) NOT NULL   COMMENT '评论的内容' ,
    `answer` TEXT NOT NULL   COMMENT '回复的内容' ,
    PRIMARY KEY (id)
)  COMMENT = '评论';
