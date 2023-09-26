"use client";
import Image from "next/image";
import styles from "../../page.module.css";
import Link from "next/link";
import { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFaceTired,
  faEyeSlash,
  faEye,
  faCheckDouble,
} from "@fortawesome/free-solid-svg-icons";
import { useRouter } from "next/navigation";
import { ACCESS_KEY, REFRESH_KEY } from "../../utils/constants";
import { Loading } from "@/app/modal/utils";

export async function registerUser(data) {
  const JsonData = JSON.stringify(data);
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JsonData,
  };

  const response = await fetch("/api/register", options);
  return await response.json();
}

export default function SignUp() {
  const [user, setUser] = useState({
    first_name: "",
    last_name: "",
    gender: "male",
    role: "customer",
    email: "",
  });
  const [errorMsg, setErrorMsg] = useState("");
  const [password, setPassword] = useState({ password1: "", password2: "" });
  const [togglePassword1, setTogglePassword1] = useState(false);
  const [togglePassword2, setTogglePassword2] = useState(false);
  const [disable, setDisable] = useState(false);
  const [openModal, setOpenModal] = useState(false);
  const { replace } = useRouter();

  const handleChange = (e) => {
    setUser({ ...user, [e.target.name]: e.target.value });
  };

  const handleCloseModel = (e) => {
    setOpenModal((prev) => !prev);
  };

  const handlePasswordChange = (e) => {
    setPassword({ ...password, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setDisable((prev) => !prev);
    if (password.password1 !== password.password2) {
      setErrorMsg("Passwords do not match");
    } else {
      const data = { ...user, password: password.password1 };
      registerUser(data).then((response) => {
        if (response?.error) {
          setErrorMsg(response.error);
        } else {
          setUser({
            first_name: "",
            last_name: "",
            gender: "male",
            role: "customer",
            email: "",
            password: "",
          });
          setPassword({ password1: "", password2: "" });
          setOpenModal((prev) => !prev);
        }
        setDisable((prev) => !prev);
      });
    }
  };

  useEffect(() => {
    const accessToken = localStorage.getItem(ACCESS_KEY);
    const refreshToken = localStorage.getItem(REFRESH_KEY);
    if (accessToken?.length > 1 && refreshToken?.length > 1) {
      replace("/");
    }
  }, [replace]);

  return (
    <>
      <header className={styles.header}>
        <div className={styles.headerLeft}>
          <Link href="/">
            <Image
              src="/store.svg"
              alt="Store logo"
              className={styles.storeLogo}
              width={100}
              height={60}
              priority
            />
          </Link>
          <h1>My Store</h1>
        </div>
      </header>

      <main className={`${styles.main} ${styles.center}`}>
        <p>
          {errorMsg ? (
            <>
              <FontAwesomeIcon icon={faFaceTired} /> &nbsp; {errorMsg}
            </>
          ) : (
            ""
          )}
        </p>
        <h1>Create an Account</h1>
        {disable ? (
          <>
            <Loading />
          </>
        ) : (
          ""
        )}

        {openModal ? (
          <>
            <div className={styles.modal}>
              <div
                className={`${styles.modalContent} ${styles.orderContainer}`}
              >
                <span className={styles.close} onClick={handleCloseModel}>
                  &times;
                </span>
                <div className={`${styles.center} ${styles.done}`}>
                  <>
                    <a href="/auth/signin"> Go to Login </a>
                    <p>
                      Thanks for registering with us, Please visit your email to
                      activate account
                    </p>
                    <FontAwesomeIcon
                      icon={faCheckDouble}
                      className={styles.doneImage}
                    />
                  </>
                </div>
              </div>
            </div>
          </>
        ) : (
          ""
        )}

        <div>
          <form className={`${styles.registerForm}`} onSubmit={handleSubmit}>
            <div className={styles.registerContainer}>
              <div>
                <input
                  type="text"
                  name="first_name"
                  placeholder="First Name"
                  onChange={handleChange}
                  value={user.first_name}
                  min={3}
                  disabled={disable}
                  required
                />
              </div>

              <div>
                <input
                  type="text"
                  name="last_name"
                  placeholder="Last Name"
                  onChange={handleChange}
                  value={user.last_name}
                  min={3}
                  disabled={disable}
                  required
                />
              </div>
              <div>
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  onChange={handleChange}
                  required
                  value={user.email}
                  disabled={disable}
                />
              </div>

              <div>
                <select
                  name="gender"
                  id="gender"
                  value={user.gender}
                  onChange={handleChange}
                  required
                  disabled={disable}
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </div>

              <div>
                <select
                  name="role"
                  id="role"
                  value={user.role}
                  onChange={handleChange}
                  required
                  disabled={disable}
                >
                  <option value="customer">Customer</option>
                  <option value="sales_rep">Sales Rep</option>
                </select>
              </div>
              <div className={styles.passwords}>
                <input
                  type={togglePassword1 ? "text" : "password"}
                  name="password1"
                  placeholder="Password"
                  onChange={handlePasswordChange}
                  value={password.password1}
                  required
                  minLength={8}
                  disabled={disable}
                  title="Password should be digits (0 to 9) or alphabets (a to z)."
                />

                <FontAwesomeIcon
                  onClick={() => setTogglePassword1(!togglePassword1)}
                  icon={togglePassword1 ? faEyeSlash : faEye}
                />
              </div>
              <div className={styles.passwords}>
                <input
                  type={togglePassword2 ? "text" : "password"}
                  name="password2"
                  placeholder="Re-type Password"
                  onChange={handlePasswordChange}
                  value={password.password2}
                  required
                  minLength={8}
                  disabled={disable}
                  title="Password should be digits (0 to 9) or alphabets (a to z)."
                />
                <FontAwesomeIcon
                  onClick={() => setTogglePassword2(!togglePassword2)}
                  icon={togglePassword2 ? faEyeSlash : faEye}
                />
              </div>
            </div>

            <div className={styles.formfooter}>
              <button disabled={disable}>
                <span>Register</span>
              </button>

              <a className={styles.forgotPassword} href="/auth/signin">
                Already have an account?
              </a>
            </div>
          </form>
        </div>
      </main>
    </>
  );
}
