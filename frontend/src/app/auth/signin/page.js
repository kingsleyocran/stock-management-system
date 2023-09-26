"use client";
import Image from "next/image";
import styles from "../../page.module.css";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFaceTired,
  faEyeSlash,
  faSignIn,
  faEye,
  faFaceSmile,
} from "@fortawesome/free-solid-svg-icons";
import { ACCESS_KEY, REFRESH_KEY } from "../../utils/constants";
import { Loading } from "@/app/modal/utils";

export default function SignIn() {
  const [user, setUser] = useState({});
  const [errorMsg, setErrorMsg] = useState("");
  const [togglePassword, setTogglePassword] = useState(false);
  const [disable, setDisable] = useState(false);
  const { push, replace } = useRouter();

  const handleChange = (e) => {
    setUser({ ...user, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const endpoint = "/api/login";
    const JsonData = JSON.stringify(user);
    setErrorMsg("");
    setDisable(true);
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JsonData,
    };

    fetch(endpoint, options).then(async (response) => {
      localStorage.removeItem(ACCESS_KEY);
      localStorage.removeItem(REFRESH_KEY);
      const res = await response.json();

      if (!res?.error) {
        localStorage.setItem(ACCESS_KEY, res?.access_token);
        localStorage.setItem(REFRESH_KEY, res?.refresh_token);
        push("/");
      } else {
        setErrorMsg(res.error);
        setDisable(false);
      }
    });
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
        {errorMsg}
        <h1>
          <FontAwesomeIcon icon={errorMsg ? faFaceTired : faFaceSmile} />
          {errorMsg ? " Aww, Error!!" : " Sign In "}
          {errorMsg ? "" : <FontAwesomeIcon icon={faSignIn} />}
        </h1>
        {disable ? (
          <>
            <Loading />
          </>
        ) : (
          ""
        )}
        <div className={styles.form}>
          <form onSubmit={handleSubmit}>
            <div>
              <input
                type="email"
                name="email"
                placeholder="Email"
                onChange={handleChange}
                disabled={disable}
                required
              />
            </div>
            <div>
              <input
                type={togglePassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                onChange={handleChange}
                disabled={disable}
                required
              />
              <FontAwesomeIcon
                onClick={() => setTogglePassword(!togglePassword)}
                icon={togglePassword ? faEyeSlash : faEye}
              />
            </div>

            <div className={styles.formfooter}>
              <button disabled={disable} type="submit">
                <span>Log In </span>
              </button>
              <div>
                <a href="/auth/signup">Create an Account</a>
                <a
                  className={styles.forgotPassword}
                  href="/auth/forgetPassword"
                >
                  Forgot Password?
                </a>
              </div>
            </div>
          </form>
        </div>
      </main>
    </>
  );
}
