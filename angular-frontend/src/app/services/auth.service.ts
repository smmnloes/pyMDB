import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Subject} from "rxjs";
import {Util} from "../util/util";
import {ToastrService} from "ngx-toastr";
import {Router} from "@angular/router";
import {UserInfo} from "../models/userInfo";
import * as jwtDecode from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private BASE_URL: string = '/api/user';

  userInfoSource = new Subject<UserInfo>();
  public $userInfoObservable = this.userInfoSource.asObservable()


  constructor(private http: HttpClient, private toastrService: ToastrService, private router: Router) {
  }

  login(email: string, password: string): void {
    let loginUrl = this.BASE_URL + '/login';
    this.http.post(loginUrl, {email: email, password: password}, Util.appJsonHeaderOptions).subscribe(
      userData => this.onSuccessfulLogin(userData),
      error => this.toastrService.error(error.error.message)
    )
  }


  onSuccessfulLogin(userData): void {
    AuthService.setAuthToken(userData);
    this.updateUserInfo(userData, true);
    this.toastrService.success("Login successful!");
    // TODO: Navigate to previous route
    this.router.navigate(['/']);
  }

  updateUserInfo(userData: any, isLoggedIn: boolean) {
    let userInfo = UserInfo.fromToken(isLoggedIn)
    this.userInfoSource.next(userInfo);
  }


  logout(): void {
    AuthService.deleteAuthToken();
    this.toastrService.success('Logout successful!')
    this.userInfoSource.next(UserInfo.loggedOutUser())
  }


  createInitialUserStatus(): void {
    let token = localStorage.getItem('token');
    if (token && AuthService.isTokenValid(token)) {
      this.userInfoSource.next(UserInfo.fromToken(true))
    } else {
      this.userInfoSource.next(UserInfo.loggedOutUser());
    }
  }


  register(email: string, password: string, username: string): void {
    let registerUrl = this.BASE_URL + '/register';
    this.http.post(registerUrl, {
      email: email,
      password: password,
      username: username
    }, Util.appJsonHeaderOptions).subscribe(
      userData => this.onSuccessfulRegistration(userData),
      error => this.toastrService.error(error.error.message)
    )
  }

  private onSuccessfulRegistration(userData) {
    AuthService.setAuthToken(userData)
    this.updateUserInfo(userData, true);
    this.toastrService.success("Registration successful! You are now logged in.")
    this.router.navigate(['/'])
  }


  private static setAuthToken(userData) {
    localStorage.setItem('token', userData.auth_token);
  }

  private static deleteAuthToken() {
    localStorage.removeItem('token');
  }

  private static isTokenValid(token: string) {
    let expireDate;
    try {
      expireDate = new Date(jwtDecode(token)['exp'] * 1000);
    } catch (e) {
      return false;
    }
    return new Date() < expireDate;
  }
}



