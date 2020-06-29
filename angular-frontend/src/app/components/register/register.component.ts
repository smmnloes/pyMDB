import {Component} from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators} from "@angular/forms";
import {ToastrService} from "ngx-toastr";


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerData: FormGroup;
  PW_MIN_LENGTH = 3;

  constructor(private authService: AuthService, private formBuilder: FormBuilder, private toastrService: ToastrService) {
    this.registerData = formBuilder.group(
      {
        email: ['', [Validators.email, Validators.required]],
        password: ['', [Validators.required, Validators.minLength(this.PW_MIN_LENGTH)]],
        passwordConfirm: '',
        username: ['', Validators.required]
      }, {validators: this.passwordConfirmValidator}
    )
  }


  passwordConfirmValidator: ValidatorFn = (control: FormGroup): ValidationErrors | null => {
    const password = control.get('password');
    const passwordConfirm = control.get('passwordConfirm');


    return password && passwordConfirm && (password.value != passwordConfirm.value) ? {'passwordsDontMatch': true} : null;
  }


  get username() {
    return this.registerData.get('username');
  }

  get email() {
    return this.registerData.get('email');
  }

  get password() {
    return this.registerData.get('password');
  }

  get passwordConfirm() {
    return this.registerData.get('passwordConfirm')
  }

  onSubmit(registerData) {
    if (this.registerData.valid) {
      this.authService.register(registerData.email, registerData.password, registerData.username);
    }
  }
}
