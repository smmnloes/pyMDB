import {Component, OnInit} from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {UserInfo} from "../../models/userInfo";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  currentUserInfo:UserInfo;
  constructor(public authService:AuthService) { }

  ngOnInit() {
    this.authService.$userInfoObservable.subscribe(userInfo => this.currentUserInfo = userInfo);
    this.authService.createInitialUserStatus()
  }

}
