import {Component} from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {FormBuilder, FormGroup} from "@angular/forms";
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerData: FormGroup;

  constructor(private authService: AuthService, private formBuilder: FormBuilder, private toastrService: ToastrService) {
    this.registerData = formBuilder.group(
      {
        email: '',
        password: '',
        passwordConfirm: '',
        username: ''
      }
    )
  }

 onSubmit(registerData) {
    if (registerData.password != registerData.passwordConfirm) {
      this.toastrService.error('"Password" and "Confirm Password" do not match')
    } else {
      this.authService.register(registerData.email, registerData.password, registerData.username);
    }
  }
}
