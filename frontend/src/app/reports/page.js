"use client";
import { useEffect, useState } from "react";
import Header from "../components/header";
import { ACCESS_KEY, REFRESH_KEY } from "../utils/constants";
import {
  getUserDetail,
  getAccessToken,
  removeToken,
  storeToken,
} from "../utils";
import { useRouter } from "next/navigation";
export default function Reports(params) {
  const [userDetails, setUserDetails] = useState({});
  const { push } = useRouter();

  useEffect(() => {
    const getUserDetailsifLoggedIn = () => {
      const token = localStorage.getItem(ACCESS_KEY);
      const refreshToken = localStorage.getItem(REFRESH_KEY);
      if (!token || !refreshToken) return push("/");

      //   if (token?.length > 0 && refreshToken?.length > 0) {
      getUserDetail().then((data) => {
        if (!data?.error) {
          setUserDetails(data);
        } else {
          getAccessToken().then((data) => {
            if (!data?.error) {
              storeToken(data);
              window.location.reload();
            } else {
              removeToken();
              push("/");
            }
          });
        }
      });
    };
    // };
    getUserDetailsifLoggedIn();
  }, [setUserDetails, push]);
  return (
    <>
      {Object.keys(userDetails).length >= 1 ? (
        <Header userDetails={userDetails} />
      ) : (
        ""
      )}
    </>
  );
}
