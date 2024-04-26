--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.0

-- Started on 2024-04-26 09:06:25

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 8 (class 2615 OID 16398)
-- Name: insurehub; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA insurehub;


ALTER SCHEMA insurehub OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16664)
-- Name: admin; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.admin (
    admin_id character varying(100) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(100) NOT NULL
);


ALTER TABLE insurehub.admin OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16671)
-- Name: admin_phone; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.admin_phone (
    admin_id character varying(100) NOT NULL,
    phone character(10) NOT NULL,
    CONSTRAINT phone_check CHECK ((phone ~ '^[0-9]{10}$'::text))
);


ALTER TABLE insurehub.admin_phone OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16850)
-- Name: claim; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.claim (
    claim_id character varying(100) NOT NULL,
    claim_amount numeric(10,2) NOT NULL,
    status character varying NOT NULL,
    date_filed date NOT NULL,
    claim_sett_dt date,
    policy_id character varying(100) NOT NULL
);


ALTER TABLE insurehub.claim OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 16988)
-- Name: claim_files; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.claim_files (
    file_id integer NOT NULL,
    claim_id character varying(255) NOT NULL,
    file_name character varying(255),
    file_data bytea,
    uploaded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE insurehub.claim_files OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16987)
-- Name: claim_files_file_id_seq; Type: SEQUENCE; Schema: insurehub; Owner: postgres
--

CREATE SEQUENCE insurehub.claim_files_file_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE insurehub.claim_files_file_id_seq OWNER TO postgres;

--
-- TOC entry 4978 (class 0 OID 0)
-- Dependencies: 235
-- Name: claim_files_file_id_seq; Type: SEQUENCE OWNED BY; Schema: insurehub; Owner: postgres
--

ALTER SEQUENCE insurehub.claim_files_file_id_seq OWNED BY insurehub.claim_files.file_id;


--
-- TOC entry 223 (class 1259 OID 16721)
-- Name: cust_phone; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.cust_phone (
    cust_id character varying(100) NOT NULL,
    phone character(10) NOT NULL,
    CONSTRAINT phone_check CHECK ((phone ~ '^[0-9]{10}$'::text))
);


ALTER TABLE insurehub.cust_phone OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16707)
-- Name: customer; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.customer (
    cust_id character varying(100) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    dob date NOT NULL,
    address character varying NOT NULL,
    agent_id character varying(100) NOT NULL
);


ALTER TABLE insurehub.customer OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16889)
-- Name: goal; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.goal (
    goal_id character varying(100) NOT NULL,
    tar_rev_per_mon character varying NOT NULL,
    target_date date NOT NULL,
    status character varying NOT NULL,
    agent_id character varying(100) NOT NULL,
    goal_name character varying(255) DEFAULT 'default_value'::character varying NOT NULL,
    action_plan character varying
);


ALTER TABLE insurehub.goal OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16877)
-- Name: payment; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.payment (
    payment_id character varying(100) NOT NULL,
    payment_amt numeric(10,2) NOT NULL,
    payment_date date NOT NULL,
    payment_method character varying NOT NULL,
    policy_id character varying(100) NOT NULL
);


ALTER TABLE insurehub.payment OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16812)
-- Name: policy; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.policy (
    policy_id character varying(100) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    tot_coverage_amt numeric(10,2) NOT NULL,
    product_id character varying(100) NOT NULL,
    status character varying(10)
);


ALTER TABLE insurehub.policy OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16920)
-- Name: policy_backup; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.policy_backup (
    policy_id character varying(100),
    start_date date,
    end_date date,
    tot_coverage_amt numeric(10,2),
    product_id character varying(100),
    status character varying(10)
);


ALTER TABLE insurehub.policy_backup OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16732)
-- Name: product; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.product (
    product_id character varying(100) NOT NULL,
    product_name character varying(100) NOT NULL,
    description character varying NOT NULL,
    admin_id character varying(100) NOT NULL,
    coverage_desc text[],
    rate_amount numeric(10,2)
);


ALTER TABLE insurehub.product OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16822)
-- Name: purchases; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.purchases (
    cust_id character varying(100) NOT NULL,
    policy_id character varying(100) NOT NULL
);


ALTER TABLE insurehub.purchases OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16682)
-- Name: relationship_manager; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.relationship_manager (
    agent_id character varying(100) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    admin_id character varying(100) NOT NULL
);


ALTER TABLE insurehub.relationship_manager OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16696)
-- Name: rm_phone; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.rm_phone (
    agent_id character varying(100) NOT NULL,
    phone character(10) NOT NULL,
    CONSTRAINT phone_check CHECK ((phone ~ '^[0-9]{10}$'::text))
);


ALTER TABLE insurehub.rm_phone OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16958)
-- Name: users; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.users (
    username character varying(255) NOT NULL,
    password text,
    name character varying(255),
    logged_in boolean,
    role character varying(255)
);


ALTER TABLE insurehub.users OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 17009)
-- Name: users_test; Type: TABLE; Schema: insurehub; Owner: postgres
--

CREATE TABLE insurehub.users_test (
    username character varying(255) NOT NULL,
    password text,
    name character varying(255),
    logged_in boolean,
    role character varying(255)
);


ALTER TABLE insurehub.users_test OWNER TO postgres;

--
-- TOC entry 4775 (class 2604 OID 16991)
-- Name: claim_files file_id; Type: DEFAULT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.claim_files ALTER COLUMN file_id SET DEFAULT nextval('insurehub.claim_files_file_id_seq'::regclass);


--
-- TOC entry 4781 (class 2606 OID 16670)
-- Name: admin admin_email_key; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.admin
    ADD CONSTRAINT admin_email_key UNIQUE (email);


--
-- TOC entry 4785 (class 2606 OID 16676)
-- Name: admin_phone admin_phone_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.admin_phone
    ADD CONSTRAINT admin_phone_pkey PRIMARY KEY (admin_id, phone);


--
-- TOC entry 4783 (class 2606 OID 16668)
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (admin_id);


--
-- TOC entry 4813 (class 2606 OID 16996)
-- Name: claim_files claim_files_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.claim_files
    ADD CONSTRAINT claim_files_pkey PRIMARY KEY (file_id);


--
-- TOC entry 4805 (class 2606 OID 16856)
-- Name: claim claim_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.claim
    ADD CONSTRAINT claim_pkey PRIMARY KEY (claim_id);


--
-- TOC entry 4797 (class 2606 OID 16726)
-- Name: cust_phone cust_phone_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.cust_phone
    ADD CONSTRAINT cust_phone_pkey PRIMARY KEY (cust_id, phone);


--
-- TOC entry 4793 (class 2606 OID 16715)
-- Name: customer customer_email_key; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.customer
    ADD CONSTRAINT customer_email_key UNIQUE (email);


--
-- TOC entry 4795 (class 2606 OID 16713)
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (cust_id);


--
-- TOC entry 4809 (class 2606 OID 17018)
-- Name: goal goal_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.goal
    ADD CONSTRAINT goal_pkey PRIMARY KEY (goal_id, goal_name);


--
-- TOC entry 4807 (class 2606 OID 16883)
-- Name: payment payment_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.payment
    ADD CONSTRAINT payment_pkey PRIMARY KEY (payment_id);


--
-- TOC entry 4801 (class 2606 OID 16816)
-- Name: policy policy_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.policy
    ADD CONSTRAINT policy_pkey PRIMARY KEY (policy_id);


--
-- TOC entry 4799 (class 2606 OID 16738)
-- Name: product product_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (product_id);


--
-- TOC entry 4803 (class 2606 OID 16826)
-- Name: purchases purchases_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.purchases
    ADD CONSTRAINT purchases_pkey PRIMARY KEY (cust_id, policy_id);


--
-- TOC entry 4787 (class 2606 OID 16690)
-- Name: relationship_manager relationship_manager_email_key; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.relationship_manager
    ADD CONSTRAINT relationship_manager_email_key UNIQUE (email);


--
-- TOC entry 4789 (class 2606 OID 16688)
-- Name: relationship_manager relationship_manager_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.relationship_manager
    ADD CONSTRAINT relationship_manager_pkey PRIMARY KEY (agent_id);


--
-- TOC entry 4791 (class 2606 OID 16701)
-- Name: rm_phone rm_phone_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.rm_phone
    ADD CONSTRAINT rm_phone_pkey PRIMARY KEY (agent_id, phone);


--
-- TOC entry 4811 (class 2606 OID 16964)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);


--
-- TOC entry 4815 (class 2606 OID 17015)
-- Name: users_test users_test_pkey; Type: CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.users_test
    ADD CONSTRAINT users_test_pkey PRIMARY KEY (username);


--
-- TOC entry 4816 (class 2606 OID 16677)
-- Name: admin_phone fk_admin; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.admin_phone
    ADD CONSTRAINT fk_admin FOREIGN KEY (admin_id) REFERENCES insurehub.admin(admin_id);


--
-- TOC entry 4817 (class 2606 OID 16691)
-- Name: relationship_manager fk_admin; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.relationship_manager
    ADD CONSTRAINT fk_admin FOREIGN KEY (admin_id) REFERENCES insurehub.admin(admin_id);


--
-- TOC entry 4822 (class 2606 OID 16739)
-- Name: product fk_admin; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.product
    ADD CONSTRAINT fk_admin FOREIGN KEY (admin_id) REFERENCES insurehub.admin(admin_id);


--
-- TOC entry 4829 (class 2606 OID 17003)
-- Name: claim_files fk_claim_files_claim_id; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.claim_files
    ADD CONSTRAINT fk_claim_files_claim_id FOREIGN KEY (claim_id) REFERENCES insurehub.claim(claim_id) ON DELETE CASCADE;


--
-- TOC entry 4821 (class 2606 OID 16934)
-- Name: cust_phone fk_cust; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.cust_phone
    ADD CONSTRAINT fk_cust FOREIGN KEY (cust_id) REFERENCES insurehub.customer(cust_id) ON DELETE CASCADE;


--
-- TOC entry 4824 (class 2606 OID 16939)
-- Name: purchases fk_cust; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.purchases
    ADD CONSTRAINT fk_cust FOREIGN KEY (cust_id) REFERENCES insurehub.customer(cust_id) ON DELETE CASCADE;


--
-- TOC entry 4819 (class 2606 OID 16970)
-- Name: customer fk_customer_email; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.customer
    ADD CONSTRAINT fk_customer_email FOREIGN KEY (email) REFERENCES insurehub.users(username);


--
-- TOC entry 4825 (class 2606 OID 16832)
-- Name: purchases fk_policy; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.purchases
    ADD CONSTRAINT fk_policy FOREIGN KEY (policy_id) REFERENCES insurehub.policy(policy_id);


--
-- TOC entry 4826 (class 2606 OID 16857)
-- Name: claim fk_policy; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.claim
    ADD CONSTRAINT fk_policy FOREIGN KEY (policy_id) REFERENCES insurehub.policy(policy_id);


--
-- TOC entry 4827 (class 2606 OID 16884)
-- Name: payment fk_policy; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.payment
    ADD CONSTRAINT fk_policy FOREIGN KEY (policy_id) REFERENCES insurehub.policy(policy_id);


--
-- TOC entry 4823 (class 2606 OID 16817)
-- Name: policy fk_product; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.policy
    ADD CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES insurehub.product(product_id);


--
-- TOC entry 4818 (class 2606 OID 16702)
-- Name: rm_phone fk_rm; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.rm_phone
    ADD CONSTRAINT fk_rm FOREIGN KEY (agent_id) REFERENCES insurehub.relationship_manager(agent_id);


--
-- TOC entry 4820 (class 2606 OID 16716)
-- Name: customer fk_rm; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.customer
    ADD CONSTRAINT fk_rm FOREIGN KEY (agent_id) REFERENCES insurehub.relationship_manager(agent_id);


--
-- TOC entry 4828 (class 2606 OID 16896)
-- Name: goal fk_rm; Type: FK CONSTRAINT; Schema: insurehub; Owner: postgres
--

ALTER TABLE ONLY insurehub.goal
    ADD CONSTRAINT fk_rm FOREIGN KEY (agent_id) REFERENCES insurehub.relationship_manager(agent_id);


-- Completed on 2024-04-26 09:06:25

--
-- PostgreSQL database dump complete
--

