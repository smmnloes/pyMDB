import {Component} from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  loginForm: FormGroup;

  constructor(private authService: AuthService, private formBuilder: FormBuilder, private toastrService: ToastrService) {
    this.loginForm = formBuilder.group(
      {
        email: ['', [Validators.email, Validators.required]],
        password: ['', Validators.required],
      }
    )
  }

  get email() {
    return this.loginForm.get('email');
  }

  get password() {
    return this.loginForm.get('password');
  }

  onSubmit(loginData): void {
    if (this.loginForm.valid) {
      this.authService.login(loginData.email, loginData.password);
    }
  }


}
