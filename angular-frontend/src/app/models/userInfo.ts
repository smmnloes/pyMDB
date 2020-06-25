import * as jwtDecode from 'jwt-decode';

export class UserInfo {
  public userName:string;
  public isAdmin: boolean;
  public isLoggedIn: boolean;

  constructor(userName: string, isAdmin: boolean, isLoggedIn: boolean) {
  this.userName = userName;
  this.isAdmin = isAdmin;
  this.isLoggedIn = isLoggedIn;
  }

  static fromToken(isLoggedIn: boolean) {
    let token = localStorage.getItem('token')
    let token_decoded = jwtDecode(token);
    let userName = token_decoded.username;
    let isAdmin = token_decoded.is_admin;
    return new UserInfo(userName, isAdmin, isLoggedIn);
  }

  static loggedOutUser() {
    return new UserInfo(null, null, false);
  }
}
