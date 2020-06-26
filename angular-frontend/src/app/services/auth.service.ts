import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Subject} from "rxjs";
import {Util} from "../util/util";
import {ToastrService} from "ngx-toastr";
import {Router} from "@angular/router";
import {map} from "rxjs/operators";
import {UserInfo} from "../models/userInfo";


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private BASE_URL: string = '/api/user';

  userInfoSource = new Subject<UserInfo>();
  public $userInfoObservable = this.userInfoSource.asObservable()


  constructor(private http: HttpClient, private toastrService: ToastrService, private router: Router) {
    this.createInitialUserStatus()
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
    let logoutUrl = this.BASE_URL + '/logout';
    this.http.post(logoutUrl, Util.appJsonHeaderOptions).subscribe(resp => {
        this.userInfoSource.next(UserInfo.loggedOutUser())
        this.toastrService.success('Logout successful!')
      }, error => {
        // Just log out the user on the client side
        this.userInfoSource.next(UserInfo.loggedOutUser())
      }
    );
  }


  createInitialUserStatus(): void {
    if (localStorage.getItem('token')) {
      let statusUrl = this.BASE_URL + '/status';
      this.http.post(statusUrl, Util.appJsonHeaderOptions).pipe(map(value => <boolean>value)).subscribe(
        isLoggedIn => this.userInfoSource.next(UserInfo.fromToken(isLoggedIn))
      );
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

}



