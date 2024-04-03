-- Table: insurehub.goal

-- DROP TABLE IF EXISTS insurehub.goal;

CREATE TABLE IF NOT EXISTS insurehub.goal
(
    goal_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    goal_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    tar_rev_per_mon character varying COLLATE pg_catalog."default" NOT NULL,
    target_date date NOT NULL,
    status character varying COLLATE pg_catalog."default" NOT NULL,
    agent_id character varying(100) COLLATE pg_catalog."default" NOT NULL,
    action_plan character varying COLLATE pg_catalog."default",
    CONSTRAINT goal_pkey PRIMARY KEY (goal_id, goal_name),
    CONSTRAINT fk_rm FOREIGN KEY (agent_id)
        REFERENCES insurehub.relationship_manager (agent_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS insurehub.goal
    OWNER to postgres;

COMMENT ON COLUMN insurehub.goal.action_plan
    IS 'Actions to achieve the goal';