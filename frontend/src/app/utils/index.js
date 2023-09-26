"use client";
import { ACCESS_KEY, REFRESH_KEY } from "./constants";
const PAGESIZE = 100;

function parseJwt(token) {
  const base64Url = token.split(".")[1];
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const jsonPayload = decodeURIComponent(
    window
      .atob(base64)
      .split("")
      .map(function (c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  return JSON.parse(jsonPayload);
}

export async function getProducts(pageNumber) {
  const data = await fetch(`/api/products?size=${PAGESIZE}&page=${pageNumber}`);
  return await data.json();
}

export async function getProductByName(name) {
  const data = await fetch(`/api/products/${name}`);
  return await data.json();
}

export async function addProduct(payload) {
  const token = await getAccessToken();
  const data = await fetch(`/api/products`, {
    method: "POST",
    body: JSON.stringify({ token: token, payload: payload }),
  });

  return await data.json();
}
export async function addProductImage(productId, image) {
  const token = await getAccessToken();
  const file = new File([image], "product.png", { type: "image/png" });
  const formData = new FormData();
  formData.append("image", file);

  const data = await fetch(`/api/products/${productId}/image`, {
    method: "POST",
    headers: {
      token: token,
    },
    body: formData,
  });
  return await data.json();
}

export async function getUserDetail() {
  const token = await getAccessToken();
  const data = await fetch(`/api/user`, {
    method: "POST",
    body: JSON.stringify({ token: token }),
  });
  return await data.json();
}

export async function getAccessToken() {
  const token = localStorage.getItem(ACCESS_KEY);
  const exp = parseJwt(token);
  const d = new Date(exp.exp * 1000);
  const now = new Date();
  // generate new access token if the token is 3mins before expiration
  const addDate = new Date(now.getTime() + 3 * 60000);
  if (addDate > d) {
    const refreshToken = localStorage.getItem(REFRESH_KEY);
    const data = await fetch(`/api/refresh`, {
      method: "POST",
      body: JSON.stringify({ refreshToken: refreshToken }),
    });
    const newToken = await data.json();
    storeToken(newToken);
    const token = localStorage.getItem(ACCESS_KEY);
    return token;
  } else {
    const token = localStorage.getItem(ACCESS_KEY);
    return token;
  }
}

export async function logOut() {
  const token = await getAccessToken();
  const data = await fetch(`/api/logout`, {
    method: "POST",
    body: JSON.stringify({ token: token }),
  });
  return await data.json();
}

export function storeToken(data) {
  localStorage.setItem(ACCESS_KEY, data?.access_token);
  localStorage.setItem(REFRESH_KEY, data?.refresh_token);
}

export function removeToken() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

export const totalQuantity = (cartList) =>
  cartList.reduce(function (acc, obj) {
    return acc + parseInt(obj.quantity);
  }, 0);

export const totalPrice = (cartList) => {
  return cartList.reduce(function (acc, obj) {
    return acc + obj.totalAmount;
  }, 0);
};

export async function makeOrder(payload) {
  const token = await getAccessToken();
  const data = await fetch(`/api/order`, {
    method: "POST",
    body: JSON.stringify({ token: token, payload: payload }),
  });
  return await data.json();
}
