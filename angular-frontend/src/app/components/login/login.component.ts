import {Component, OnInit} from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {FormBuilder, FormGroup} from "@angular/forms";
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup;

  constructor(private authService: AuthService, private formBuilder: FormBuilder, private toastrService: ToastrService) {
    this.loginForm = formBuilder.group(
      {
        email: '',
        password: ''
      }
    )
  }

  ngOnInit(): void {
  }


  onSubmit(loginData): void {
    this.authService.login(loginData.email, loginData.password);
  }


}
