"use client";
import Image from "next/image";
import styles from "../../page.module.css";
import Link from "next/link";
import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFaceTired,
  faSignIn,
  faInbox,
  faFaceLaughBeam,
  faFaceSmile,
} from "@fortawesome/free-solid-svg-icons";

export default function ForgetPassword() {
  const [email, setEmail] = useState({});
  const [disable, setDisable] = useState(false);
  const [displaySendMsg, setDisplaySendMsg] = useState(false);

  const handleChange = (e) => {
    setEmail({ ...email, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setDisplaySendMsg(true);
    // setDisable(true);
    // loginUser(user).then((res) => {
    //   console.log("responses", res);
    //   if (!res?.error) {
    //     addItemToStorage("my_store_access_token", res?.access_token);
    //     addItemToStorage("my_store_refresh_token", res?.refresh_token);
    //     push("/");
    //   } else {
    //     setDisable(false);
    //   }
    // });
  };

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
        {displaySendMsg ? (
          <>
            <h1>
              <FontAwesomeIcon icon={faFaceLaughBeam} />
              {""} Email Sent &nbsp;
            </h1>

            <div className={styles.form}>
              <div className={styles.recoverPasswordInput}>
                <div>
                  <h3>
                    Password reset link has been sent to your email address.{" "}
                    <br />
                    Please check your email inbox &nbsp;
                    <FontAwesomeIcon icon={faInbox} />
                  </h3>
                  <br /> <br />
                  <Link href="/auth/signin">
                    <h3> Go to Login Page </h3> &nbsp;
                    <FontAwesomeIcon icon={faSignIn} />
                  </Link>
                </div>
              </div>
            </div>
          </>
        ) : (
          <>
            <h1 className={styles.forgetHeader}>
              Hi, Let's Get Your Password Back &nbsp;
              <FontAwesomeIcon icon={faFaceSmile} />
            </h1>

            <div className={styles.form}>
              <div className={styles.recoverPasswordInput}>
                <h3 className={styles.forgetHeader}>
                  {" "}
                  Please Enter Your Email Address{" "}
                </h3>
                <div>
                  <form onSubmit={handleSubmit}>
                    <div>
                      <input
                        type="email"
                        name="email"
                        value={email?.email}
                        placeholder="Fill in your email address"
                        onChange={handleChange}
                        disabled={disable}
                        required
                      />
                    </div>

                    <div className={styles.formfooter}>
                      <button disabled={disable} type="submit">
                        <span>Submit </span>
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </>
  );
}
